---
license: cc-by-nc-4.0
task_categories:
- graph-ml
- text-retrieval
language:
- en
tags:
- finance
- knowledge-graph
- financial-entities
- sec-filings
- Form 10-K
- FinReflectKG
- 10-k-filings
- financial-nlp
- temporal-knowledge-graph
- S&P500
- triples
- GraphRag
pretty_name: FinReflectKG
size_categories:
- 10M<n<100M
---

# Dataset Card for FinReflectKG

A comprehensive financial knowledge graph dataset extracted from S&P 500 companies' 10-K SEC filings spanning 2014-2024, containing **17.51 million normalized triplets** with full textual context.

## Dataset Details

### Dataset Description

**Curated by:** [Domyn](https://www.domyn.com/)

**Language(s):** English

**License:** CC-BY-NC-4.0

FinReflectKG is a large-scale financial knowledge graph dataset that provides structured representations of financial relationships, entities, and temporal information extracted from regulatory filings. Each triplet represents a structured fact in the format `(entity, relationship, target)` with temporal bounds and rich contextual information.

### Dataset Sources

**Paper:** [FinReflectKG: Agentic Construction and Evaluation of Financial Knowledge Graphs](https://arxiv.org/pdf/2508.17906)

## Key Features

- **17.51M triplets** across 743 S&P 500 companies
- **10+ years** of temporal coverage (2014-2024)  
- **Full text context** for each triplet
- **Normalized entities** and relationships
- **Temporal information** with start/end dates
- **Rich metadata** including source document information

## Dataset Structure

Each row contains a single triplet with the following fields:

### Core Triplet Components
- `triplet_id`: Unique identifier for each triplet
- `entity`: Named entity (normalized, e.g., "aapl")
- `entity_type`: Entity category (ORG, PERSON, GPE, etc.)
- `relationship`: Relationship type (normalized, e.g., "discloses", "operates_in")
- `target`: Target entity (normalized)
- `target_type`: Target entity category
- `start_date`: Relationship start date (Month YYYY format)
- `end_date`: Relationship end date (Month YYYY or "default_end_timestamp")
- `extraction_type`: Extraction method ("default" or "extracted")

### Document Metadata
- `ticker`: Company ticker symbol (e.g., "aapl", "msft")
- `year`: Filing year
- `source_file`: Original PDF filename
- `page_id`: PDF page identifier  
- `chunk_id`: Text chunk identifier

### Context & Features
- `chunk_text`: Full text context surrounding the triplet
- `triplet_length`: Length of triplet text representation
- `chunk_text_length`: Length of context text
- `has_context`: Whether contextual text is available

## Temporal Information

### Temporal Fields Explained

FinReflectKG employs sophisticated temporal extraction to capture when relationships occur or are valid. The temporal information consists of:

#### Start Date & End Date
- **Format**: "Month YYYY" (e.g., "January 2024", "March 2023")
- **Purpose**: Captures the temporal validity period of each relationship

#### Default Timestamps
When explicit temporal information cannot be reliably extracted from the text context:
- **`default_start_timestamp`**: Used when no explicit start date is mentioned or inferable
- **`default_end_timestamp`**: Used when no explicit end date is mentioned or inferable

**Examples**:
- **Extracted**: "Environmental spending was approximately $21 million in fiscal 2014" → `start_date`: "January 2014", `end_date`: "December 2014"
- **Default**: "Cintas depends on multiple suppliers" → `start_date`: "January 2014" (filing year), `end_date`: "default_end_timestamp"

### Extraction Type Classification

The `extraction_type` field indicates the reliability and source of temporal information:

#### "extracted"
- **When**: Both start_date AND end_date are successfully extracted from the text
- **Example**: Financial metrics with specific fiscal periods, dated announcements, time-bounded events

#### "default"  
- **When**: Either start_date OR end_date (or both) uses default values
- **Example**: General operational relationships, ongoing business activities without specified timeframes


## Example Usage

### Loading the Dataset

```python
from datasets import load_dataset

# Load the complete dataset
dataset = load_dataset("domyn/FinReflectKG")

# Access the data
triplets = dataset["train"]
print(f"Dataset size: {len(triplets):,} triplets")

# Example triplet
example = triplets[0]
print(f"Entity: {example['entity']}")
print(f"Relationship: {example['relationship']}")  
print(f"Target: {example['target']}")
print(f"Context: {example['chunk_text'][:200]}...")
```

### Filtering by Company

```python
# Filter for Apple (AAPL) triplets
apple_data = dataset["train"].filter(lambda x: x["ticker"] == "aapl")
print(f"Apple triplets: {len(apple_data):,}")
```

### Filtering by Time Period

```python
# Filter for recent years (2022-2024)
recent_data = dataset["train"].filter(lambda x: x["year"] >= 2022)
print(f"Recent triplets: {len(recent_data):,}")
```

### Filtering by Relationship Type

```python
# Find all "discloses" relationships
disclosure_data = dataset["train"].filter(lambda x: x["relationship"] == "discloses")
print(f"Disclosure triplets: {len(disclosure_data):,}")
```

## Entity Types

The dataset includes various entity types relevant to financial documents:

- **ORG**: Filing Company (The public company that is the subject of the 10-K filing)
- **ORG_GOV**: Government bodies (e.g., United States Government)
- **ORG_REG**: Domestic or international regulatory bodies (e.g., SEC, Federal Reserve, ECB)
- **GPE**: Countries, states, or cities mentioned in geographic operations or risks
- **PERSON**: Key individuals (e.g., CEO, CFO)
- **COMP**: External companies referenced in the filing, including competitors, suppliers, customers, or partners
- **PRODUCT**: Products or services (e.g., iPhone, AWS)
- **EVENT**: Material events such as pandemics, natural disasters, M&A events
- **SECTOR**: Sectors or industries relevant to the filer ORG or COMP entities (e.g., Technology, Healthcare, Financials)
- **ECON_IND**: Quantitative metrics that reflect economic trends or conditions (e.g., Inflation Rate, GDP Growth, Unemployment Rate, Interest Rate, Consumer Confidence Index)
- **FIN_INST**: Tradable financial assets or liabilities (e.g., bonds, derivatives, options)
- **FIN_MARKET**: Financial indices and market dynamics (e.g., S&P 500, Dow Jones)
- **CONCEPT**: Abstract concepts or theories (e.g., Artificial Intelligence, Digital Transformation, Circular Economy)
- **RAW_MATERIAL**: Essential raw materials (e.g., Lithium)
- **LOGISTICS**: Supply chain and logistics entities (e.g., Ports)
- **ACCOUNTING_POLICY**: Key accounting policies (e.g., revenue recognition, lease accounting, goodwill impairment)
- **RISK_FACTOR**: Documented risks (e.g., market risk, supply chain risk, cybersecurity risk, geopolitical risk)
- **LITIGATION**: Legal disputes or proceedings including lawsuits, regulatory investigations, or settlements disclosed in the 10-K
- **SEGMENT**: Internal divisions or business segments of the filer ORG (e.g., Cloud segment, North America retail)
- **FIN_METRIC**: Financial metrics or values (e.g., Net Income, EBITDA, Long-Term Debt, CapEx, R&D Expense)
- **ESG_TOPIC**: Environmental, Social, and Governance themes (e.g., Carbon Emissions, DEI, Renewable Energy, Climate Risk)
- **MACRO_CONDITION**: Qualitative or thematic macroeconomic trends that affect the company or industry (e.g., Recession, Inflationary Pressures, Tightening Monetary Policy, Economic Uncertainty, Labor Shortages)
- **REGULATORY_REQUIREMENT**: Specific regulations or legal frameworks (e.g., Basel III, SEC rules, GDPR)
- **COMMENTARY**: Statements or disclosures from company management (e.g., outlooks, explanations, guidance)

## Relationship Types

The dataset includes comprehensive relationship types for financial knowledge graphs:

- **Has_Stake_In**: Indicates full or partial ownership or equity interest (e.g., ORG owns SEGMENT or has stake in COMP)
- **Announces**: Publicly discloses or communicates (e.g., ORG announces PRODUCT launch or ESG_TOPIC initiative)
- **Operates_In**: Indicates operational geography or market presence (e.g., ORG operates in GPE)
- **Introduces**: Rolls out or implements a new product, policy, or segment (e.g., ORG introduces PRODUCT or ACCOUNTING_POLICY)
- **Produces**: Manufactures or develops a product or service (e.g., ORG produces PRODUCT)
- **Regulates**: Exerts control or regulatory oversight (e.g., ORG_REG regulates ORG)
- **Involved_In**: Specifies direct involvement in an event such as a merger, acquisition, or litigation
- **Impacted_By**: Indicates that the entity was materially affected by a major event (e.g., Amazon impacted_by COVID-19)
- **Impacts**: Specifies the broad influence or effect an entity or event has on financial performance, market trends, or other key outcomes
- **Positively_Impacts**: Contributes to positive outcomes (e.g., ESG_TOPIC positively impacts FIN_METRIC)
- **Negatively_Impacts**: Contributes to adverse outcomes (e.g., RISK_FACTOR negatively impacts FIN_METRIC)
- **Related_To**: Indicates a connection or relationship
- **Member_Of**: Indicates formal affiliation or group membership (e.g., COMP is member of FIN_MARKET index)
- **Invests_In**: Allocates financial or strategic capital (e.g., ORG invests in COMP or ESG_TOPIC)
- **Increases**: Denotes a growth or rise in value or activity (e.g., ORG increases CapEx or debt)
- **Decreases**: Denotes a decline in value or activity (e.g., ORG decreases headcount or R&D spend)
- **Depends_On**: Requires support or shows reliance on another entity (e.g., ORG depends on RAW_MATERIAL or COMP)
- **Causes_Shortage_Of**: Indicates supply constraint driven by an event or condition (e.g., EVENT causes shortage of RAW_MATERIAL)
- **Affects_Stock**: Indicates direct influence on stock price or valuation (e.g., RISK_FACTOR affects_stock of ORG)
- **Stock_Decline_Due_To**: Specifies factor causing drop in stock price (e.g., MACRO_CONDITION stock_decline_due_to ORG)
- **Stock_Rise_Due_To**: Specifies factor causing increase in stock price (e.g., ESG_TOPIC stock_rise_due_to ORG)
- **Market_Reacts_To**: Indicates market response to external events or disclosures (e.g., FIN_MARKET market_react_to EVENT)
- **Discloses**: Reveals or reports (e.g., ORG discloses FIN_METRIC, ESG_TOPIC, or RISK_FACTOR)
- **Faces**: Encounters legal or regulatory challenges (e.g., ORG faces LITIGATION or REGULATORY_REQUIREMENT)
- **Guides_On**: Provides management commentary or forecast (e.g., COMMENTARY guides_on FIN_METRIC or MACRO_CONDITION)
- **Complies_With**: Meets regulatory or policy requirements (e.g., ORG complies_with REGULATORY_REQUIREMENT)
- **Subject_To**: Indicates entity is governed or affected by (e.g., ORG subject_to ACCOUNTING_POLICY or REGULATORY_REQUIREMENT)
- **Supplies**: Indicates vendor or supplier relationship (e.g., COMP supplies RAW_MATERIAL to ORG)
- **Partners_With**: Indicates formal or strategic collaboration (e.g., ORG partners_with COMP for PRODUCT)

## Data Quality

The dataset has undergone extensive cleaning and validation:

- **99.08% clean dates** in proper "Month YYYY" format
- **Normalized entities** and relationships using lemmatization
- **Deduplicated triplets**
- **Filtered invalid data**
- **Comprehensive validation** of data structure and integrity

## Temporal Coverage

**📊 TOTAL TRIPLETS: 17,513,372**  
**📅 YEAR RANGE: 2014-2024**  
**🏢 COMPANIES: 743**

| Year Range | Triplet Count | Exact Count | Companies |
|------------|---------------|-------------|-----------|
| 2014-2018  | 7.55M         | 7,549,552   | 743       |
| 2019-2021  | 5.04M         | 5,043,004   | 743       |
| 2022-2024  | 4.92M         | 4,920,816   | 743       |
| **TOTAL**  | **17.51M**    | **17,513,372** | **743** |

## Applications

This dataset is suitable for:

### Research Applications
- **Financial NLP**: Named entity recognition, relation extraction
- **Knowledge Graph Construction**: Building financial knowledge bases
- **Temporal Analysis**: Studying financial relationships over time
- **Risk Assessment**: Analyzing risk factors and their evolution
- **Compliance Research**: Understanding regulatory relationships

### Industry Applications  
- **Financial Intelligence**: Automated analysis of SEC filings
- **Due Diligence**: Comprehensive company relationship mapping
- **ESG Analysis**: Environmental, social, governance insights
- **Market Research**: Understanding competitive landscapes
- **Regulatory Technology**: Compliance and risk monitoring

## Data Source

The dataset is derived from S&P 500 companies' 10-K annual reports filed with the SEC.


## Ethical Considerations

- **Public data**: All source data is publicly available SEC filings
- **No personal information**: Focus on corporate and financial entities
- **Regulatory compliance**: Respects SEC disclosure requirements
- **Research use**: Intended for academic and research purposes

## Citation

If you use this dataset in your research, please cite:

```bibtex
@article{arun2025finreflectkg,
  title={FinReflectKG: Agentic Construction and Evaluation of Financial Knowledge Graphs},
  author={Arun, Abhinav and Dimino, Fabrizio and Agarwal, Tejas Prakash and Sarmah, Bhaskarjit and Pasquali, Stefano},
  journal={arXiv preprint arXiv:2508.17906},
  year={2025},
  url={https://arxiv.org/pdf/2508.17906}
}
```

## Dataset Creation

For detailed information about the dataset creation process, methodology, and evaluation, please refer to the attached paper: [FinReflectKG: Agentic Construction and Evaluation of Financial Knowledge Graphs](https://arxiv.org/pdf/2508.17906).

## Dataset Card Contact

Reetu Raj Harsh (reeturaj.harsh@domyn.com)
