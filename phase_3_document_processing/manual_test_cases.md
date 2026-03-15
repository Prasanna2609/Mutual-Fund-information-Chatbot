# Phase 3 - Manual Text Processing Validations

Use these validation checks against the output `phase_3_document_processing/processed_chunks.json` to verify that critical financial metrics are securely captured and not lost during chunking.

You can `cat processed_chunks.json | grep -i "term"` to spot-check:

## Validation 1: NAV Values
Check that standard NAV declarations exist for the extracted schemes. Example search: `"NAV"` or `"Net Asset Value"`

## Validation 2: Expense Ratio
Ensure the percentage and associated context for expense ratios persist. Example search: `"Expense ratio"` or `"%"`

## Validation 3: Exit Load
Verify exit penalties and their duration requirements are parsed. Example search: `"Exit Load"`

## Validation 4: Minimum SIP & Min Investment
Guarantee that users will get the right baseline numbers. Example search: `"Minimum SIP"`

## Validation 5: Benchmark Index
Ensure that index comparisons (e.g. NIFTY 50, BSE 100) are intact. Example search: `"Benchmark"`

## Validation 6: Risk Level
Check if the "Very High Risk" or similar labels appear on these equity funds. Example search: `"Riskometer"` or `"Risk level"`

## Validation 7: Fund Manager
Look for names and tenures of managers. Example search: `"Fund Manager"`

## Validation 8: AUM
Look for "AUM" or "Assets Under Management". Example search: `"AUM"`
