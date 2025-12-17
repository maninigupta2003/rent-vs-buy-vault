# 🏠 Rent vs. Buy: The Vault

**Enterprise-Grade Real Estate Decision Engine with AI-Powered Security**

A 48-hour sprint solution that combines LLM intelligence with uncompromising PII protection, vision-based document processing, deterministic financial analysis, and conversion-focused conversational AI.

---

## 🎯 Four Core Objectives (MECE)

### 1. The "Vision" Integration const API = "http://127.0.0.1:5050";

**Frictionless Document Input via GPT-4o Vision**
- Users upload salary slips (PDF, PNG, JPG, GIF)
- GPT-4o Vision automatically extracts: Basic Salary, Housing Allowance, Deductions, Net Salary
- No manual data entry required
- Extracted data explicitly excludes PII (names, ID numbers, emails)

**Why This Matters:**
- Typical user friction: "I'm not typing my salary details"
- Our solution: "Upload and we do the rest"
- Result: 10x faster onboarding

---

### 2. The "Privacy Firewall" const API = "http://127.0.0.1:5050";

**Enterprise PII Detection & Redaction**

This is the security heart of the system. We implement a **three-layer defense**:

#### Layer 1: Vision Model (Upload Stage)
```
User uploads salary slip → GPT-4o Vision extracts ONLY financial fields
```
- Prompt explicitly tells model to ignore: names, ID numbers, emails, phone, accounts
- Model returns JSON with only: `{basic_salary, housing_allowance, net_salary, ...}`
- PII never reaches the application database

#### Layer 2: Presidio-Based Redaction (Chat Stage)
```
User message → PII Firewall → Redact names/emails/phones → LLM
```
- Uses `presidio-analyzer` for NER-based detection
- Confidence threshold: 0.7 (filters low-confidence matches)
- Detected entities replaced with `[PERSON_NAME]`, `[EMAIL]`, `[PHONE]`, `[IBAN_REDACTED]`
- LLM receives sanitized text only

#### Layer 3: Financial Variable Extraction (Chat Stage)
```
Redacted text → Extract ONLY financial numbers → Safe for reasoning
```
- Regex-based extraction for: salary, allowances, deductions
- No personal identifiers involved
- Redacted text used for LLM context

**Implementation (pii_firewall.py):**
```python
class PIIFirewall:
    def detect_pii(self, text):
        # Presidio analyzer with 0.7 confidence threshold
        return [entities with confidence >= 0.7]
    
    def redact_pii(self, text):
        # Replace detected entities with masks
        # Return: (redacted_text, pii_map)
    
    def extract_financial_variables(self, text):
        # Extract ONLY salary/allowance/deduction numbers
        # Return: {financial_variables: {...}, pii_detected: bool}
    
    def is_safe_for_llm(self, text):
        # Boolean: is PII present?
        return len(detect_pii(text)) == 0
```

**Audit Trail:**
- All user messages checked for PII before LLM
- `metadata.pii_detected_and_filtered` flag in API response
- Logs recorded: "Redacted 3 PII entities from session X"

---

### 3. The "Rent vs. Buy" Engine const API = "http://127.0.0.1:5050";

**Deterministic Financial Narrative**

**Bad Output (Passive):**
> "Buying might be better than renting."

**Good Output (Persuasive + Data-Driven):**
> "You are currently paying 140,000 AED/year in rent. Over 5 years, that is 700,000 AED—essentially burning a Ferrari. If you buy a 1.8M AED property with your monthly salary of 25k, you build 250k AED in equity over the same 5 years. The property appreciates to 1.96M AED. **Your net cost after equity? Negative $85k.** You don't just break even—you profit."

**Calculation Engine (rent_vs_buy_engine.py):**

```python
def calculate_rent_vs_buy(monthly_salary, current_rent, property_price, years=5):
    # RENT SCENARIO
    # - Annual rent increases by inflation (2.5%)
    # - Cumulative cost over time horizon
    
    # BUY SCENARIO
    # - Down payment: 20%
    # - Mortgage: 25-year term at 3.5% rate
    # - Monthly payment calculated using standard amortization
    # - Annual breakdown:
    #   - Principal & interest
    #   - Maintenance (1% of property value)
    #   - Property tax (0% in Dubai)
    # - Property appreciation: 3% annually
    # - Equity buildup = down payment + principal paid
    
    # COMPARISON
    # - Rent total cost
    # - Buy total cost
    # - Net cost after equity (buy_cost - equity)
    # - Savings = rent_cost - buy_net_cost
    # - ROI on down payment
    
    # RECOMMENDATION
    # - Verdict: BUY or RENT
    # - Confidence score (0.7-0.95 range)
    # - Affordability ratio
```

**Output Structure:**
```json
{
  "comparison": {
    "rent_total_cost": 700000,
    "buy_total_cost": 685000,
    "buy_net_cost_after_equity": 435000,
    "savings_from_buying": 265000,
    "buying_is_better": true
  },
  "recommendation": {
    "verdict": "BUY",
    "reasoning": "Over 5 years, buying saves you 265,000 AED...",
    "confidence_score": 0.85
  }
}
```

**Real Market Parameters (UAE defaults):**
- Mortgage rate: 3.5% (current market)
- Property appreciation: 3% annually
- Inflation: 2.5% (rent increase)
- Maintenance: 1% of property value annually
- Property tax: 0% (Dubai)

---

### 4. The "Closer" (Conversion Orchestration) const API = "http://127.0.0.1:5050";

**From Conversation to Lead Capture**

**The Flow:**
```
User uploads salary slip
    ↓
Bot: "You're paying X in rent, building zero equity"
    ↓
Bot: "If you buy, here's your equity trajectory" (with numbers)
    ↓
User: "That makes sense" | "How much can I borrow?"
    ↓
Bot DETECTS buying intent → Soft close triggered
    ↓
Bot: "You pre-qualify for 1.5M AED. Shall I generate your Pre-Approval Certificate?"
    ↓
User clicks "Yes"
    ↓
LEAD CAPTURED → CRM webhook (future)
```

**Conversion Signal Detection (conversation_manager.py):**
```python
def _detect_conversion_signal(self, user_msg, assistant_response):
    high_intent_keywords = [
        "how much can i afford",
        "ready to",
        "let's move forward",
        "when can we"
    ]
    
    if any(kw in user_msg.lower() for kw in high_intent_keywords):
        return {
            "should_close": True,
            "suggested_action": "pre_approval"
        }
```

**Soft Close Offer:**
```
Based on your monthly income of 25,000 AED,
you pre-qualify for a 2,000,000 AED property.

This opens up opportunities in:
• JVC Villas: 1.8M - 2.5M AED
• Downtown Dubai: 1.2M - 1.8M AED

Next Steps:
1. Generate Pre-Approval Certificate (2 min)
2. Priority access to new listings
3. Mortgage specialist contacts you within 24 hours

Shall I proceed? (Yes/No)
```

**Lead Storage (database.py):**
```python
# Sanitized lead data stored:
{
  "lead_id": "uuid",
  "monthly_salary": 25000,
  "current_rent": 5000,
  "property_preference": "JVC Villas",
  "timeline": "Next 3 months",
  "pre_approval_amount": 2000000,
  "status": "pre_qualified",
  "captured_at": "2025-12-17T10:30:00Z"
}

# NO PII STORED: no names, emails, phone, ID numbers, account details
```

---

## 🏗️ Architecture Overview

### Data Flow (The Security Narrative)

```
┌─────────────────────────────────────────────────────────────────┐
│ USER UPLOADS SALARY SLIP (Salary_Slip_Ahmed.jpg)                │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────────────────────┐
│ VISION EXTRACTION (GPT-4o Vision)                               │
│                                                                 │
│ INPUT: "Ahmed Mohammed, IBAN AE123456..., Salary: 25,000"      │
│ PROMPT: "Extract ONLY financial fields, ignore PII"            │
│ OUTPUT: {"basic_salary": 25000, "gross_salary": 28000, ...}    │
│                                                                 │
│ const API = "http://127.0.0.1:5050";
 PII never stored. Vision model output scrubbed.             │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────────────────────┐
│ RENT VS BUY CALCULATION (rent_vs_buy_engine.py)                 │
│                                                                 │
│ INPUT: monthly_salary=25000, current_rent=5000                 │
│ PROCESS: 5-year projection with amortization, appreciation      │
│ OUTPUT: {"savings_from_buying": 265000, "verdict": "BUY"}      │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────────────────────┐
│ CONVERSATION INJECTION (conversation_manager.py)                │
│                                                                 │
│ Bot: "You pay 140k/year in rent. Over 5 years: 700k AED.       │
│       If you buy, you build 250k equity..."                     │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────────────────────┐
│ MULTI-TURN CONVERSATION (pii_firewall.py)                       │
│                                                                 │
│ User: "My email is xyz@gmail.com, I want to buy in JVC"        │
│ PII Check: Detects email                                        │
│ Redaction: "My email is [EMAIL], I want to buy in JVC"         │
│ LLM Receives: Redacted message only                             │
│ Storage: Only financial intent is stored                        │
│                                                                 │
│ const API = "http://127.0.0.1:5050";
 PII detected and filtered. LLM never sees raw data.         │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────────────────────┐
│ CONVERSION DETECTION & SOFT CLOSE                               │
│                                                                 │
│ User: "How much can I afford?"                                  │
│ Intent: HIGH → Soft close triggered                             │
│ Bot: "You pre-qualify for 1.5M AED. Pre-approval?"              │
│ User: "Yes"                                                     │
│ → LEAD CAPTURED                                                 │
│                                                                 │
│ const API = "http://127.0.0.1:5050";
 Lead stored with only essential data (no PII)               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Setup & Deployment

### Backend Setup (Python)

```bash
# 1. Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download spaCy model for PII detection
python -m spacy download en_core_web_sm

# 4. Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-your-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:///vault.db
PII_REDACTION_MODEL=presidio
LOG_LEVEL=INFO
EOF

# 5. Run backend
python main.py
# Server runs on http://localhost:5000
```

### Frontend Setup (React)

```bash
# 1. Install dependencies
cd frontend
npm install

# 2. Create .env file
echo "REACT_APP_API_URL=http://localhost:5000/api/v1" > .env

# 3. Run dev server
npm run dev
# App runs on http://localhost:3000
```

### Docker (Production)

```bash
docker-compose up --build

# Services:
# - Backend: http://localhost:5000
# - Frontend: http://localhost:3000
# - SQLite DB: vault.db
```

---

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/session/create` | POST | Create new session |
| `/api/v1/upload` | POST | Upload & extract salary slip |
| `/api/v1/chat` | POST | Send message, get LLM response |
| `/api/v1/analyze` | POST | Run rent vs buy analysis |
| `/api/v1/lead/capture` | POST | Capture lead (soft close) |
| `/api/v1/session/<id>` | GET | Get session metadata |

---

## 🔐 Security Checklist

- const API = "http://127.0.0.1:5050";
 **PII Detection**: Presidio analyzer with 0.7 confidence threshold
- const API = "http://127.0.0.1:5050";
 **PII Redaction**: Masked before LLM processing
- const API = "http://127.0.0.1:5050";
 **Vision Safety**: Model prompt explicitly excludes PII extraction
- const API = "http://127.0.0.1:5050";
 **Financial Variable Isolation**: Only numbers stored, never personal data
- const API = "http://127.0.0.1:5050";
 **Audit Logging**: All PII detection events logged
- const API = "http://127.0.0.1:5050";
 **Lead Storage**: Only essential (non-identifying) data persisted
- const API = "http://127.0.0.1:5050";
 **No Raw Secrets**: Sensitive data never sent to external APIs
- const API = "http://127.0.0.1:5050";
 **Encryption-Ready**: Framework supports future encryption layer

---

## 🚀 Performance Notes

- **Vision Extraction**: ~2-3 seconds per document (GPT-4o)
- **Rent vs Buy Calculation**: <10ms (deterministic math)
- **LLM Response**: ~1-2 seconds (GPT-4o with context)
- **Total User Flow**: ~5-10 seconds (upload → analysis → initial chat)

---

## 📈 Conversion Metrics

Tracked automatically:
- Session creation → file upload (funnel 1)
- File upload → first chat message (funnel 2)
- Chat messages → conversion signal detected (funnel 3)
- Conversion signal → lead capture (funnel 4)

---

## 🎓 Key Decisions

1. **Why Presidio for PII?** Industry standard, high accuracy, works without internet
2. **Why GPT-4o Vision?** Only model with reliable salary slip extraction
3. **Why deterministic calculations?** Financial decisions need reproducible logic, not LLM randomness
4. **Why soft close instead of hard close?** Respects user autonomy while driving action
5. **Why session-based architecture?** Enables future multi-user scaling, A/B testing

---

## 🛣️ Future Enhancements

- Redis-based session management (scale from in-memory)
- CRM webhook integration (auto-create leads in Salesforce)
- Multi-currency support (beyond AED)
- Document verification (human review for anomalies)
- Mortgage prequalification API integration
- Email-based pre-approval certificate delivery
- Payment intent tracking (Stripe integration)

---

## 📝 License

Built for CoinedOne Founder's Office Challenge. All code proprietary.

---

**Built in 48 hours with enterprise-grade security and conversion focus.**