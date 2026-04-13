import sys
import os
import csv
import argparse
# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anonymizer.diagnostics import diagnose_span

def print_row(id, target, status, details=""):
    print(f"{id:<10} | {target:<20} | {status:<15} | {details}")

def main():
    parser = argparse.ArgumentParser(description="Run diagnostics on regression cases.")
    parser.add_argument("--file", default="tests/regression/cases.csv", help="Path to cases CSV file")
    parser.add_argument("--verbose", action="store_true", help="Show detailed candidates info")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found.")
        sys.exit(1)
        
    print("\n" + "="*80)
    print(f"{'ID':<10} | {'TARGET':<20} | {'STATUS':<15} | {'REASON / DETAILS'}")
    print("-" * 80)
    
    total = 0
    passed = 0
    
    with open(args.file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            case_id = row.get("id", "unk")
            text = row.get("text", "")
            target = row.get("expected", "")
            
            result = diagnose_span(text, target)
            
            status = result["status"].upper()
            details = ""
            
            if status == "FOUND":
                details = f"Detected as {result['final_result'].entity_type.value}"
                passed += 1
            elif status == "FILTERED":
                details = f"Filters: {', '.join(result['filters'])}"
            elif status == "SHADOWED":
                sb = result["shadowed_by"]
                details = f"Shadowed by '{sb['text']}' ({sb['type']}) from {sb['source']}"
            elif status == "NER_REGEX_FAILURE":
                details = "Not caught by NER or Regex patterns"
            elif status == "NOT_IN_TEXT":
                details = "Target string not found in input text"
            
            print_row(case_id, target, status, details)
            
            if args.verbose:
                if result["candidates"]:
                    print("           Candidates:")
                    for c in result["candidates"]:
                        print(f"             - '{c['text']}' ({c['type']}) [{c['source']}] span:{c['span']}")

    print("-" * 80)
    print(f"Summary: {passed}/{total} passing cases.")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
