import argparse
import subprocess

def load_list_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="Run tasks with or without subtasks with a specified model.")

    parser.add_argument(
        "--max_iterations", 
        type=int, 
        default=5, 
        help="Max number of iterations per task or subtask. Default is 5."
    )
    parser.add_argument(
        "--provider", 
        required=True, 
        help="Provider/framework to access model with. e.g. openai"
    )
    parser.add_argument(
        "--model", 
        required=True, 
        help="Model to request from provider/base_url. e.g. gpt-4-0613"
    )
    parser.add_argument(
        "--tokenizer", 
        help="Tokenizer to use with model (if needed). e.g. cl100k_base"
    )
    parser.add_argument(
        "--unguided_mode", 
        action="store_true", 
        default=False, 
        help="Whether to run on unguided mode."
    )
    parser.add_argument(
        "--max_input_tokens", 
        type=int, 
        default=6000, 
        help="The limit on the number of input tokens sent to the model; truncates if it exceeds this value. Default 6000."
    )
    parser.add_argument(
        "--max_output_tokens", 
        type=int, 
        default=2000, 
        help="The limit on the number of output tokens that can be received from the model. Default 2000."
    )
    parser.add_argument(
        "--task_list", 
        type=str, 
        default='benchmarks.txt', 
        required=False, 
        help="The list of tasks to run on. See benchmarks.txt for reference."
    )
    parser.add_argument(
        "--responses_to_keep", 
        type=int, 
        default=3, 
        help="Number of responses to keep."
    )
    parser.add_argument(
        "--observations_to_keep", 
        type=int, 
        default=3, 
        help="Number of observations to keep."
    )
    parser.add_argument(
        "--helm",
        action="store_true",
        help="Run the agent using the CRFM-HELM API",
        default=False,
    )
    parser.add_argument(
        "--azure",
        action="store_true",
        help="Run the agent using the Azure OpenAI API",
        default=False,
    )
    parser.add_argument(
        "--localhost",
        action="store_true",
        help="Run the docker environment with `--network=host`",
        default=False,
    )

    args = parser.parse_args()

    cleanup_command = "docker rm -f $(docker ps -aq)"
    if args.task_list:
        items = load_list_from_file(args.task_list)
    else:
        items = load_list_from_file('benchmarks.txt') 

    for item in items:
        base_command = (
            f"./run_task.sh --task_dir '{item}' "
            f"--max_iterations {args.max_iterations} "
            f"--max_input_tokens {args.max_input_tokens} "
            f"--max_output_tokens {args.max_output_tokens} "
            f"--provider '{args.provider}' "
            f"--model '{args.model}' "
            f"{'--tokenizer '+args.tokenizer if args.tokenizer else ''}"
            f"--responses_to_keep {args.responses_to_keep} "
            f"--observations_to_keep {args.observations_to_keep} "
            f"{'--helm ' if args.helm else ''}"
            f"{'--azure ' if args.azure else ''}"
            f"{'--unguided_mode ' if args.unguided_mode else ''}"
            f"{'--localhost ' if args.localhost else ''}"
        )

        print(f"Running command: {base_command}")
        subprocess.run(base_command, shell=True)
        print(f"Cleaning up all Docker containers with: {cleanup_command}")
        subprocess.run(cleanup_command, shell=True)
        print("----------------------------------------------")  
        print("All logs are saved to the logs directory based on task_name.")  
if __name__ == "__main__":
    main()
