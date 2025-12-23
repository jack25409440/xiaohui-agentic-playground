# Agentic Workflow Design Patterns

A comprehensive exploration and comparison of 5 different agentic workflow design patterns for LLM-based systems, demonstrated through a news classification task.

**Author:** Xiaohui Chen

## 📋 Overview

This notebook implements and evaluates five distinct agentic workflow patterns using the AG News dataset for multi-class text classification. Each pattern represents a different approach to orchestrating LLM agents for complex tasks.

### Design Patterns Covered

| # | Pattern | Description | LLM Calls |
|---|---------|-------------|-----------|
| 1 | **Prompt Chaining** | Sequential pipeline where each step builds on the previous | 3 |
| 2 | **Routing** | Intelligent router directs input to specialized expert agents | 2 |
| 3 | **Parallelization** | Multiple agents process simultaneously, results aggregated by code | 4 |
| 4 | **Orchestrator-Worker** | LLM orchestrator coordinates workers, LLM synthesizer combines results | 6 |
| 5 | **Evaluator-Optimizer** | Generator + critical evaluator with iterative refinement loop | 2-6 |

## 🗂️ Dataset

**AG News** - A news article classification dataset from HuggingFace

- **Training set:** 120,000 articles
- **Test set:** 7,600 articles (100 samples used for experiments)
- **Categories:**
  - 🌍 **World** - International news and events
  - ⚽ **Sports** - Athletic events, teams, players
  - 💼 **Business** - Companies, markets, economy
  - 🔬 **Sci/Tech** - Science and technology news

## 🔧 Models Used

| Provider | Models |
|----------|--------|
| **Anthropic** | Claude Sonnet 4, Claude Sonnet 4.5, Claude Haiku 4.5, Claude Opus 4.5 |
| **OpenAI** | GPT-5-mini, GPT-5.1 |

## 📊 Results Summary

### Overall Performance

| Rank | Design Pattern | Accuracy | F1 (Macro) | LLM Calls |
|------|----------------|----------|------------|-----------|
| 🥇 | **Prompt Chaining** | **83.0%** | **0.822** | 3 |
| 🥈 | Routing | 82.0% | 0.806 | 2 |
| 🥉 | Evaluator-Optimizer | 81.0% | 0.804 | 2-6 |
| 4 | Orchestrator-Worker | 80.0% | 0.792 | 6 |
| 5 | Parallelization | 72.0% | 0.717 | 4 |

### Cost-Efficiency (Calls per 1% Accuracy)

| Pattern | Efficiency |
|---------|------------|
| **Routing** | 2.4 (most efficient) |
| Evaluator-Optimizer | 2.9 |
| Prompt Chaining | 3.6 |
| Parallelization | 5.6 |
| Orchestrator-Worker | 7.5 (least efficient) |

## 🏗️ Pattern Details

### 1. Prompt Chaining (83.0% Accuracy)

A sequential 3-step pipeline:

```
INPUT → Step 1: Extract → Step 2: Analyze → Step 3: Classify → OUTPUT
         (Claude         (GPT-5.1)         (Claude
          Sonnet 4)                         Haiku 4.5)
```

- **Step 1:** Entity & keyword extraction from raw text
- **Step 2:** Domain signal analysis for each category
- **Step 3:** Final classification decision

**Strengths:** Highest accuracy, interpretable intermediate outputs, structured decomposition

---

### 2. Routing (82.0% Accuracy)

An intelligent router directs each article to a specialized expert:

```
           ┌→ Sports Expert (Haiku 4.5)
INPUT → Router → Business Expert (Sonnet 4) → OUTPUT
     (GPT-5-mini) └→ Science/World Expert (Sonnet 4.5)
```

**Strengths:** Most cost-efficient, excellent specialized performance (science_world_expert: 96.4% accuracy)

---

### 3. Parallelization (72.0% Accuracy)

Four category detectors run simultaneously, aggregated by confidence voting:

```
          ┌→ World Detector ────┐
INPUT → ──┼→ Sports Detector ───┼→ Confidence Voting → OUTPUT
          ├→ Business Detector ─┤   (Python Code)
          └→ Sci/Tech Detector ─┘
```

**Weaknesses:** 15% fallback rate, simple voting struggles with ambiguous cases

---

### 4. Orchestrator-Worker (80.0% Accuracy)

LLM orchestrator creates customized instructions for workers, LLM synthesizer makes final decision:

```
INPUT → Orchestrator → 4 Workers (parallel) → Synthesizer → OUTPUT
        (GPT-5-mini)   (4× Haiku 4.5)        (GPT-5.1)
```

**Insights:** Complex pipeline with high cost (6 calls) but marginal benefit over simpler approaches

---

### 5. Evaluator-Optimizer (81.0% Accuracy)

Generator produces classification, evaluator critically reviews and may reject for refinement:

```
INPUT → Generator ⇄ Evaluator → OUTPUT
        (GPT-5.1)   (Opus 4.5)
        ↑___________↓
         (feedback loop, max 3 iterations)
```

**Findings:** 90% approved on first iteration; self-correction actually decreased accuracy by 1%

## 🔍 Key Insights

### Common Challenge: Business vs Sci/Tech Confusion

All patterns struggle with the same classification boundary. Tech company articles about products get misclassified as Business:

| Pattern | Business Precision | Business Over-prediction |
|---------|-------------------|--------------------------|
| All Patterns | 43-52% | +9 to +16 articles |

### When to Use Each Pattern

| Use Case | Recommended Pattern |
|----------|---------------------|
| Highest accuracy needed | **Prompt Chaining** |
| Cost is primary concern | **Routing** |
| Need interpretable steps | **Prompt Chaining** |
| Domain expertise varies widely | **Routing** |
| Need multiple perspectives | **Parallelization** |
| Complex reasoning with verification | **Evaluator-Optimizer** |

## 🚀 Getting Started

### Prerequisites

```bash
pip install openai anthropic datasets scikit-learn python-dotenv
```

### Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Running the Notebook

1. Open `agentic_systems.ipynb` in Jupyter or VS Code
2. Run cells sequentially to execute each design pattern
3. Results and metrics are displayed after each pattern's evaluation

## 📁 Structure

```
1-agentic-workflow/
├── README.md                 # This file
└── agentic_systems.ipynb     # Main notebook with all implementations
```

## 📈 Future Improvements

1. **Better Business/Sci/Tech disambiguation:** Add explicit instructions for tech company article classification
2. **Two-stage classification:** First Business vs Non-Business, then subdivide
3. **Few-shot examples:** Provide examples distinguishing financial vs product-focused tech articles
4. **Ensemble approach:** Combine Prompt Chaining with Routing for ambiguous cases

## 📚 References

- [AG News Dataset (HuggingFace)](https://huggingface.co/datasets/sh0416/ag_news)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [OpenAI API](https://platform.openai.com/docs/)

