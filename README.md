# SRE Haiku Horror Generator

Demo application for AI/SRE conference talks showcasing GPU scheduling with KAI Scheduler.

## What it does
Generates darkly humorous haikus about SRE/DevOps incidents using OpenAI API.

## Usage
```bash
docker run -e OPENAI_API_KEY=your-key -p 5000:5000 piotrzan/sre-haiku-generator
```

## Demo Purpose
Shows fractional GPU allocation (50%) via KAI Scheduler on Kubernetes.