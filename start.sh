docker image build -t suvambasak/orchestrator:latest .
docker container run -v ~/.ssh:/root/.ssh -it --rm suvambasak/orchestrator:latest