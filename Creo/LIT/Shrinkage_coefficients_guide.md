# 🌍 Shrinkage Coefficients Guide for HTS Casting

## 📋 Concept: Ratio to Minimum Shrinkage

### 1.1 Base Concept
For casting mark **VCh50** (Volumetric Shrinkage Coefficient 50):
- **Module ratio**: 1 : 1.2 : 1.4
  - 1 = casting modulus (baseline)
  - 1.2 = minimum riser modulus for adequate feeding
  - 1.4 = recommended riser modulus with safety factor

This means: riser modulus ≥ 1.2 × casting modulus, and for reliability: ≥ 1.4 × casting modulus

### 1.2 How Other Systems Calculate

**Chinese System:**
- Ratio: 1 : 1.15 : 1.3 (for USADKA_P = 1.0%)
- Simplified based on shrinkage percentage

**American System (AWS D10.1):**
- Ratio: 1 : (1.1–1.3) : (1.2–1.5)
- Additional safety factor 1.1–1.3 added
- Per steel grade Z-constanta

**European System (EN 1563):**
- Ratio: 1 : 1.25 : 1.45 (carbon steels)
- 1 : 1.3 : 1.5 (alloy steels)
- Standardized per EN tables

**Turkish System:**
- Ratio: 1 : 1.25 : 1.35
- Adaptation of GOST 14953-80
- Consideration of furnace type

## 📊 Global Coefficients Table per Alloy

### 2.1 Shrinkage Modulus Ratio per Alloy Type

| Alloy Type | Minimum | Recommended | Maximum | Notes |
|-----------|---------|-------------|---------|-------|
| **Carbon Steels** | | | | |
| Low carbon (C20, C30, C40) | 1.10 | 1.20 | 1.35 | Better fluidity |
| Medium carbon (C45, C50, C60) | 1.15 | 1.25 | 1.45 | Standard range |
| High carbon (C70, C80, C90) | 1.20 | 1.35 | 1.55 | Harder to feed |
| **Low-Alloy Steels** | | | | |
| 2H13, 3H13, 4H13 (Cr13) | 1.15 | 1.30 | 1.50 | Chromium steels |
| 20H3A, 30H3A, 40H3A (CrNi) | 1.20 | 1.35 | 1.55 | Chromium-nickel |
| 30HM, 40HM, 50HM (Mo, V) | 1.25 | 1.40 | 1.60 | Mo, V alloyed |
| **Stainless Steels** | | | | |
| 08X18N10T (austenitic) | 1.10 | 1.20 | 1.30 | High fluidity |
| 08X13, 10X13 (ferritic) | 1.15 | 1.25 | 1.35 | Moderate fluidity |
| 022X18N10M2T (duplex) | 1.20 | 1.35 | 1.50 | Complex structure |
| **Special Alloys** | | | | |
| Heat-resistant | 1.30 | 1.50 | 1.70 | High temperatures |
| Wear-resistant (V, Cr, Mo) | 1.20 | 1.40 | 1.60 | Abrasion resistance |

### 2.2 Economic Efficiency Impact

| Alloy Type | At ratio 1.2 | At ratio 1.4 | Efficiency change |
|-----------|-------------|-------------|-----------------|
| Carbon steels | 88–92% | 85–89% | -3–5% |
| Low carbon steels | 90–94% | 87–90% | -2–4% |
| Medium carbon steels | 89–93% | 86–90% | -3–5% |
| High carbon steels | 85–89% | 82–86% | -4–6% |
| Low-alloy steels | 90–93% | 87–90% | -3–4% |
| Stainless austenitic | 92–95% | 89–92% | -3–5% |
| Duplex steels | 88–92% | 85–89% | -4–6% |

### 2.3 Profitability vs Scrap Analysis

| Scenario | Riser Ratio | Metal Waste | Scrap Rate | Profitability | Recommendation |
|----------|-------------|-------------|------------|---------------|----------------|
| **Small castings** (< 500 kg) | 1.2 | Low (8–10%) | 2–3% | High (92–95%) | Optimal economy |
| **Medium castings** (500–2000 kg) | 1.25 | Medium (10–14%) | 3–5% | Medium-High (88–92%) | Balanced approach |
| **Large castings** (> 2000 kg) | 1.3–1.4 | High (14–20%) | 5–8% | Medium (85–88%) | Safety first |
| **Critical components** | 1.3–1.5 | Very high (20–30%) | 8–12% | Low-Medium (80–85%) | Quality priority |
| **High-volume production** | 1.15–1.2 | Very low (5–8%) | 1–2% | Very High (94–97%) | Economy priority |

### 2.4 Regional Comparison of Coefficients

| Region | Carbon Steels | Low-Alloy | Stainless | Special |
|--------|--------------|-----------|-----------|---------|
| **China** | 1.10–1.30 | 1.15–1.35 | 1.10–1.25 | Simplified, metal saving |
| **USA (AWS D10.1)** | 1.20–1.50 | 1.25–1.55 | 1.15–1.35 | Detailed, quality-first |
| **Europe (EN 1563)** | 1.25–1.50 | 1.30–1.55 | 1.20–1.45 | Standardized |
| **Turkey** | 1.15–1.40 | 1.20–1.45 | 1.15–1.30 | GOST adaptation, local conditions |

## 🎯 Practical Recommendations

### 3.1 Choosing the Riser Ratio Algorithm

1. **Identify steel grade** and its USADKA_P (shrinkage %)
2. **Select base coefficient** from table 2.1
3. **Apply modifiers:**
   - Casting size: large → +0.05–0.10
   - Geometry complexity: high → +0.05–0.10
   - Quality requirements: critical → +0.05–0.10
   - Production experience: novice → use recommended value
4. **Check economic efficiency** from table 2.2
5. **Adjust if needed** within regional allowances

### 3.2 Universal Recommendations

- **Start value**: coefficient 1.25 suits 80% of cases
- **Conservative approach**: use recommended coefficient from table on first design
- **Adaptive approach**: after 3–5 castings with same alloy, adjust per real results
- **Documentation**: always fix used coefficient per casting for future reference

### 3.3 Key Takeaways

- **Ratio 1:1.2:1.4** is the classic baseline for VCh50 castings
- **Higher ratios** (1.3–1.4) = more metal in risers, less scrap, lower economic efficiency
- **Lower ratios** (1.1–1.2) = less metal in risers, higher scrap risk, higher economic efficiency
- **Optimal balance** for most cases: 1.2–1.3
- **Always document** the used coefficient per casting for future process improvement
- **Regional standards** differ but converge around 1.2–1.4 range

## 📁 Files Created/Updated

- `Shrinkage_coefficients_guide.md` — comprehensive guide above
- Key data integrated into `HTS_calculations_guide.md` (Section 14)
- Supporting data in `liteika_hts_mm_relations.md` (SAFE, ST, PRIB blocks)
- Regional skill files: `SKILL_lit_hts_china.md`, `SKILL_lit_hts_aws.md`, `SKILL_lit_hts_en.md`, `SKILL_lit_hts_turkey.md`

---
*Guide created: 24.09.2026 by Cline*
*Coverage: shrinkage coefficients per alloy, global comparison, practical recommendations*