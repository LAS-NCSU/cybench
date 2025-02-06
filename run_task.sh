#!/bin/bash

set -e

if [[ -z ${DOCKER_NETWORK_DRIVER} ]]; then
	# default network is bridge
	export DOCKER_NETWORK_DRIVER="bridge"
fi

# Validate current directory for volume mounting
if [[ "$(basename "$(pwd)")" != "cybench" ]]; then
	echo "Error: Please run this script from the cybench directory."
	exit 1
fi

get_task_dir() {
	for arg in "$@"; do
		if [[ ${arg} == "--task_dir" ]]; then
			echo "${2}"
		fi
	done
}
task_dir=$(get_task_dir "$@")

container_name="cybench"
image_name="cybench/cybench:latest"
network_name="shared_net"

echo "before docker rm"

docker rm -f "${container_name}"

echo "after docker rm, before network_name"

# Run --network "host" if --localhost set
for arg in "$@"; do
	if [[ ${arg} == "--localhost" ]]; then
		network_name="host"
	fi
done
if [[ "${network_name}" != "host" ]]; then 

	# Create shared network if it doesn't exist
	if ! docker network ls | grep -q "${network_name}"; then
		echo "Creating Docker network: ${network_name}"
		docker network create "${network_name}"
	fi
fi

echo "after network_name, before start_docker.sh"

# if the task has a start_docker.sh, execute it
if [[ -f "${task_dir}/start_docker.sh" ]]; then
	echo "Executing start_docker.sh script for the task"
	echo "${task_dir}"
	"${task_dir}/start_docker.sh"
fi

echo "after start_docker.sh, before docker run"

echo "Running Docker container"
docker run \
	--name "${container_name}" \
	-it \
	--pull always \
	--privileged \
	--network "${network_name}" \
	--cgroupns host \
	-v "$(pwd)/agent":/app/agent:ro \
	-v "$(pwd)/run_task.py":/app/run_task.py:ro \
	--env-file=.env \
	"${image_name}" "$@" | tee /tmp/benchmark-latest.log

echo "after docker run"

# Get exit status of `docker run`
exit_status=${PIPESTATUS[0]}

docker cp "${container_name}:/app/logs/." "$(pwd)/logs/"

docker rm -f "${container_name}"

if [[ -f "${task_dir}/stop_docker.sh" ]]; then
	echo "Executing stop_docker.sh script for the task"
	"${task_dir}/stop_docker.sh"
fi

if [[ ${exit_status} -ne 0 ]]; then
	echo "Error: Task failed."
	exit 1
fi
