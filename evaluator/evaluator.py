from typing import List, Dict, Any
from models.data_models import TaskEntry, ExtractionResult, EvaluationResult

class Evaluator:
    def __init__(self):
        pass

    def _exact_match(self, pred: Dict[str, str], gold: Dict[str, str]) -> bool:
        return (pred['subject'].lower() == gold['subject'].lower() and
                pred['relation'].lower() == gold['relation'].lower() and
                pred['object'].lower() == gold['object'].lower())

    def _calculate_f1(self, precision: float, recall: float) -> float:
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)

    def evaluate(self, entry: TaskEntry, result: ExtractionResult) -> EvaluationResult:
        gold_triples = [{"subject": t.subject, "relation": t.relation, "object": t.object} for t in entry.gold_triples]
        pred_triples = [{"subject": t.subject, "relation": t.relation, "object": t.object} for t in result.triples]
        pred_schemas = [{"subject": s.subject, "object": s.object} for s in result.schemas]

        matched = sum(
            1 for pred in pred_triples
            if any(self._exact_match(pred, gold) for gold in gold_triples)
        )

        precision = matched / len(pred_triples) if pred_triples else 0.0
        recall    = matched / len(gold_triples) if gold_triples else 0.0
        f1        = self._calculate_f1(precision, recall)

        return EvaluationResult(
            entry_id=entry.entry_id,
            input_text=entry.input_text,
            gold_triples=gold_triples,
            pred_triples=pred_triples,
            pred_schemas=pred_schemas,
            is_correct=(f1 == 1.0),
            precision=precision,
            recall=recall,
            f1=f1,
        )
