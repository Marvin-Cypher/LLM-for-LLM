# Uploading Legal LLM Benchmark Dataset to Hugging Face

This guide walks you through uploading your benchmark dataset to Hugging Face Hub.

## Prerequisites

1. **Hugging Face Account**
   - Create account at: https://huggingface.co/join
   - This is free and takes 1 minute

2. **Install Required Packages**
   ```bash
   pip install huggingface-hub datasets pandas
   ```

## Step 1: Login to Hugging Face

First, login using the CLI:

```bash
huggingface-cli login
```

You'll be prompted for your access token:
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name (e.g., "legal-llm-benchmark")
4. Select "Write" permission
5. Copy the token
6. Paste it when prompted in the terminal

## Step 2: Upload Dataset

Run the upload script:

```bash
cd /Users/marvin/legal-llm-benchmark
python3 scripts/upload_to_huggingface.py
```

This will:
- Load all 40 Phase 2 contract tasks
- Load associated contract documents
- Create a Hugging Face dataset
- Upload to `Marvin-Cypher/legal-llm-benchmark`
- Generate and upload a dataset card (README)

## Step 3: Verify Upload

Visit your dataset page:
```
https://huggingface.co/datasets/Marvin-Cypher/legal-llm-benchmark
```

You should see:
- Dataset preview with your tasks
- README with benchmark information
- Download buttons
- Dataset viewer

## Step 4: Test Loading

Test that others can load your dataset:

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("Marvin-Cypher/legal-llm-benchmark")

# Check Phase 2 tasks
print(f"Total Phase 2 tasks: {len(dataset['phase2_contract_tasks'])}")

# View a sample task
sample = dataset['phase2_contract_tasks'][0]
print(f"Task: {sample['title']}")
print(f"Type: {sample['task_type']}")
print(f"Instruction: {sample['instruction'][:200]}...")
```

## What Gets Uploaded

### Phase 2 Contract Tasks (40 tasks)
Each task includes:
- `task_id`: Unique identifier
- `contract_id`: Associated contract
- `task_type`: add_clause, modify, review, redline, summarize
- `title`: Human-readable title
- `instruction`: Full task instruction
- `evaluation_criteria`: JSON array of criteria
- `input_file`: Contract filename
- `contract_text`: Full contract text
- `context`: Metadata (parties, dates, contract type)

## Customizing the Repository Name

If you want a different repository name, edit line 134 in `scripts/upload_to_huggingface.py`:

```python
# Change from:
repo_id = "Marvin-Cypher/legal-llm-benchmark"

# To your preferred name:
repo_id = "YourUsername/your-dataset-name"
```

## Making Dataset Private

By default, the dataset will be public. To make it private, add `private=True`:

Edit `scripts/upload_to_huggingface.py` line 141:

```python
create_repo(repo_id, repo_type="dataset", exist_ok=True, private=True)
```

## Adding More Data

To add Phase 1 tasks or benchmark results:

1. Create a new function in `scripts/upload_to_huggingface.py` to load the data:
   ```python
   def load_phase1_tasks():
       # Load your Phase 1 tasks from wherever they are
       pass
   ```

2. Add it to the DatasetDict:
   ```python
   dataset_dict = DatasetDict({
       "phase2_contract_tasks": phase2_dataset,
       "phase1_tasks": phase1_dataset,  # Add this
   })
   ```

## Updating the Dataset

To update the dataset after initial upload:

```bash
# Make your changes to the data
python3 scripts/upload_to_huggingface.py
```

The script will automatically update the existing dataset.

## Dataset Card (README)

The script automatically generates a comprehensive README with:
- Dataset description
- Data structure and fields
- Usage examples
- Benchmark results
- Citation information

You can customize it by editing the `create_dataset_card()` function in `scripts/upload_to_huggingface.py`.

## Troubleshooting

### Authentication Error
```
Error: Invalid token
```
**Solution**: Run `huggingface-cli login` again with a valid token

### Repository Already Exists
```
Repository already exists
```
**Solution**: This is fine! The script will update the existing repo. Or change the repo_id to a new name.

### Missing Dependencies
```
ModuleNotFoundError: No module named 'datasets'
```
**Solution**:
```bash
pip install huggingface-hub datasets pandas
```

### File Not Found
```
FileNotFoundError: [Errno 2] No such file or directory: 'phase2_documents/tasks/...'
```
**Solution**: Make sure you run the script from the repository root:
```bash
cd /Users/marvin/legal-llm-benchmark
python3 scripts/upload_to_huggingface.py
```

## Next Steps

After uploading:

1. **Add Badge to README**: Add the dataset badge to your GitHub README:
   ```markdown
   [![Dataset](https://img.shields.io/badge/🤗%20Hugging%20Face-Dataset-yellow)](https://huggingface.co/datasets/Marvin-Cypher/legal-llm-benchmark)
   ```

2. **Share on Social Media**: Announce your dataset on Twitter/LinkedIn with the Hugging Face link

3. **Update Paper**: Add the Hugging Face dataset link to your paper's Data Availability section

4. **Monitor Usage**: Check your dataset's downloads and views on the Hugging Face dashboard

## Example Output

When successful, you'll see:

```
📦 Preparing Legal LLM Benchmark Dataset for Hugging Face...

1️⃣ Loading Phase 2 contract tasks...
   ✅ Loaded 40 Phase 2 contract tasks

2️⃣ Creating Hugging Face datasets...
   ✅ Created dataset with 40 total tasks

3️⃣ Creating/Updating repository: Marvin-Cypher/legal-llm-benchmark
   ✅ Repository created/verified

4️⃣ Uploading dataset to Hugging Face Hub...
   ✅ Dataset uploaded successfully!

5️⃣ Creating dataset card (README.md)...
   ✅ Dataset card saved locally as 'huggingface_dataset_card.md'
   ✅ Dataset card uploaded to Hub

🎉 Dataset successfully uploaded!
📍 View at: https://huggingface.co/datasets/Marvin-Cypher/legal-llm-benchmark

📖 Usage:
   from datasets import load_dataset
   dataset = load_dataset("Marvin-Cypher/legal-llm-benchmark")
```

## Support

For issues with the upload script:
- Check this guide first
- Open an issue at: https://github.com/Marvin-Cypher/LLM-for-LLM/issues

For Hugging Face Hub issues:
- Hugging Face docs: https://huggingface.co/docs/datasets
- Hugging Face forum: https://discuss.huggingface.co/
