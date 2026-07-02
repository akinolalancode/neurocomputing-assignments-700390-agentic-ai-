"""
Assignment 4: Agentic AI Application
Student: AKINOLA, Lanre Olusegun
Student ID: 12349031
Course: 700.390 Advanced Topics in Neurocomputing

A simple agent that reads a question, picks the right tool,
calls it, observes the result, and gives a final answer.
"""

import re
import math
import time
import json
import os
import requests

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False


# ===========================================================
# TOOL 1: Web Search (adapted from search_api.py)
# ===========================================================

def search_web(query, max_results=5):
    """Search the internet using DuckDuckGo."""
    if not DDGS_AVAILABLE:
        return {"success": False, "error": "ddgs not installed.", "results": []}
    try:
        with DDGS(timeout=10) as ddgs:
            raw = list(ddgs.text(query, max_results=max_results))
        if not raw:
            return {"success": False, "error": "No results found.", "results": []}
        results = [
            {"title": r.get("title", ""), "body": r.get("body", ""), "url": r.get("href", "")}
            for r in raw[:max_results]
        ]
        return {"success": True, "results": results}
    except Exception as e:
        return {"success": False, "error": str(e), "results": []}


# ===========================================================
# TOOL 2: Currency Conversion (Frankfurter API)
# ===========================================================

def convert_currency(amount, from_currency, to_currency):
    """Convert an amount from one currency to another using Frankfurter API."""
    try:
        from_c = from_currency.upper()
        to_c = to_currency.upper()
        # Use frankfurter.app endpoint (same provider as frankfurter.dev)
        url = f"https://api.frankfurter.app/latest?from={from_c}&to={to_c}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        rate = data["rates"][to_c]
        return {
            "success": True,
            "from": from_c,
            "to": to_c,
            "rate": rate,
            "amount": amount,
            "converted": round(amount * rate, 4),
            "date": data.get("date", "")
        }
    except KeyError:
        return {"success": False, "error": f"Unknown currency code: {to_currency}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to Frankfurter API."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_multiple_rates(base, targets):
    """Get several exchange rates at once (used for currency comparison)."""
    try:
        symbols = ",".join([t.upper() for t in targets])
        url = f"https://api.frankfurter.app/latest?from={base.upper()}&to={symbols}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {
            "success": True,
            "base": data["base"],
            "rates": data["rates"],
            "date": data.get("date", "")
        }
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to Frankfurter API."}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ===========================================================
# TOOL 3: Calculator
# ===========================================================

def calculate(expression):
    """Evaluate a simple arithmetic expression safely."""
    try:
        # Only allow math operations — no access to builtins or globals
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return {"success": True, "expression": expression, "result": round(float(result), 6)}
    except ZeroDivisionError:
        return {"success": False, "error": "Division by zero."}
    except Exception as e:
        return {"success": False, "error": f"Cannot evaluate: {e}"}


# ===========================================================
# AGENT LOGIC
# ===========================================================

def select_tool(question):
    """
    Decide which tool to use based on keywords in the question.
    The agent does this automatically without asking the user.

    Returns one of:
      'search'              -- DuckDuckGo web search
      'currency'            -- single currency conversion
      'multi_currency'      -- compare several currencies
      'currency_calculate'  -- get rate then compute an amount
    """
    q = question.lower()
    currency_words = ["eur", "usd", "gbp", "jpy", "chf", "currency", "currencies"]
    has_currency = any(w in q for w in currency_words)

    # Multi-step: need a rate AND a calculation
    if has_currency and any(k in q for k in ["how much is", "how much are", "equals", "equal to"]):
        return "currency_calculate"

    # Comparison: at least two currencies mentioned
    if has_currency and any(k in q for k in ["compare", "vs", "versus", "and"]):
        found = re.findall(r'\b(eur|usd|gbp|jpy|chf)\b', q)
        if len(set(found)) >= 2:
            return "multi_currency"

    # Simple single conversion
    if has_currency and any(k in q for k in ["convert", "exchange", "rate", "to usd", "to eur", "to gbp"]):
        return "currency"

    # Default: web search
    return "search"


def _parse_currencies_and_amount(question):
    """Helper: extract currency codes and the first number from a question."""
    q = question.upper()
    currencies = re.findall(r'\b(EUR|USD|GBP|JPY|CHF)\b', q)
    amounts = re.findall(r'\b(\d+(?:\.\d+)?)\b', q)
    amount = float(amounts[0]) if amounts else 1.0
    return amount, currencies


def run_agent(question):
    """
    Main agent loop.
    Prints the trace: question -> tool -> observation -> final answer.
    """
    print("=" * 65)
    print(f"QUESTION : {question}")

    t0 = time.time()
    tool_name = select_tool(question)
    print(f"TOOL     : {tool_name}")

    answer = ""
    tool_result = None

    # ---- currency: single conversion ----
    if tool_name == "currency":
        amount, currencies = _parse_currencies_and_amount(question)
        from_c = currencies[0] if len(currencies) > 0 else "EUR"
        to_c   = currencies[1] if len(currencies) > 1 else "USD"

        tool_result = convert_currency(amount, from_c, to_c)
        print(f"OBSERVE  : rate={tool_result.get('rate')}, converted={tool_result.get('converted')}, date={tool_result.get('date')}")

        if tool_result["success"]:
            answer = (
                f"{amount} {tool_result['from']} = {tool_result['converted']} {tool_result['to']}  "
                f"(1 {tool_result['from']} = {tool_result['rate']} {tool_result['to']}, "
                f"as of {tool_result['date']})"
            )
        else:
            answer = f"Currency conversion failed: {tool_result['error']}"

    # ---- multi_currency: compare rates ----
    elif tool_name == "multi_currency":
        _, currencies = _parse_currencies_and_amount(question)
        base    = currencies[0] if currencies else "EUR"
        targets = list(dict.fromkeys(c for c in currencies[1:] if c != base))
        if not targets:
            targets = ["USD", "GBP"]

        tool_result = get_multiple_rates(base, targets)
        print(f"OBSERVE  : base={tool_result.get('base')}, rates={tool_result.get('rates')}")

        if tool_result["success"]:
            lines = [f"Live exchange rates for 1 {tool_result['base']} (date: {tool_result['date']}):"]
            for cur, rate in tool_result["rates"].items():
                lines.append(f"  1 {tool_result['base']} = {rate} {cur}")
            answer = "\n".join(lines)
        else:
            answer = f"Failed to get rates: {tool_result['error']}"

    # ---- currency_calculate: rate then multiply ----
    elif tool_name == "currency_calculate":
        _, currencies = _parse_currencies_and_amount(question)
        base   = currencies[0] if currencies else "EUR"
        target = currencies[-1] if len(currencies) > 1 else "USD"
        # Look for "how much is 250 EUR" pattern first; fall back to largest number
        how_much = re.search(r'how much (?:is|are)\s+(\d+(?:\.\d+)?)', question, re.IGNORECASE)
        if how_much:
            amount = float(how_much.group(1))
        else:
            all_nums = re.findall(r'\b(\d+(?:\.\d+)?)\b', question)
            amount = max(float(n) for n in all_nums) if all_nums else 1.0

        # Step 1 — get rate
        rate_result = convert_currency(1, base, target)
        print(f"OBSERVE  [step 1 - rate ] : 1 {base} = {rate_result.get('rate')} {target}")

        if rate_result["success"]:
            rate = rate_result["rate"]
            expr = f"{amount} * {rate}"

            # Step 2 — calculate
            calc_result = calculate(expr)
            print(f"OBSERVE  [step 2 - calc ] : {expr} = {calc_result.get('result')}")

            if calc_result["success"]:
                answer = (
                    f"{amount} {base} = {calc_result['result']} {target}  "
                    f"(calculation: {amount} x {rate} = {calc_result['result']}, "
                    f"date: {rate_result['date']})"
                )
            else:
                answer = f"Calculation error: {calc_result['error']}"
            tool_result = {"rate_step": rate_result, "calc_step": calc_result}
        else:
            answer = f"Could not fetch exchange rate: {rate_result['error']}"
            tool_result = rate_result

    # ---- search: web search ----
    else:
        tool_result = search_web(question)
        n = len(tool_result.get("results", []))
        print(f"OBSERVE  : {n} result(s) returned from DuckDuckGo")

        if tool_result["success"] and tool_result["results"]:
            snippets = [r["body"].strip() for r in tool_result["results"] if r.get("body")]
            combined = " ".join(snippets[:2])
            if len(combined) > 700:
                combined = combined[:700] + "..."
            sources = [r["url"] for r in tool_result["results"] if r.get("url")]
            answer = combined
            if sources:
                answer += f"\n[Source: {sources[0]}]"
        else:
            answer = f"Search returned no usable results. {tool_result.get('error', '')}"

    elapsed = round(time.time() - t0, 2)

    # Shorten for terminal display
    display_answer = answer if len(answer) <= 300 else answer[:300] + "..."
    print(f"ANSWER   : {display_answer}")
    print(f"TIME     : {elapsed}s")
    print()

    return {
        "question": question,
        "tool": tool_name,
        "answer": answer,
        "time_seconds": elapsed
    }


# ===========================================================
# MAIN — run all 7 example questions
# ===========================================================

QUESTIONS = [
    "What is the capital of Austria, and what is its current population?",
    "Convert 100 EUR to USD.",
    "Search for recent information about Agentic AI and summarize it in three sentences.",
    "If 1 EUR equals X USD, how much is 250 EUR in USD?",
    "Find information about MCP and explain why it is useful for agent tools.",
    "Compare EUR to GBP and USD using live exchange-rate data.",
    "What is Tesla's current stock price?"
]


if __name__ == "__main__":
    all_results = []

    for q in QUESTIONS:
        result = run_agent(q)
        all_results.append(result)

    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/agent_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print(f"{'#':<3} {'Question':<48} {'Tool':<22} {'Time':>6}")
    print("-" * 65)
    for i, r in enumerate(all_results, 1):
        q_short = r["question"][:46]
        print(f"{i:<3} {q_short:<48} {r['tool']:<22} {r['time_seconds']:>5.2f}s")
    print()
    print("Results saved to results/agent_results.json")
