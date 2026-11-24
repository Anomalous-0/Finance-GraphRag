(set-logic QF_NRA)
(set-option :produce-models true)

(declare-const computed_capital_expenditures Real)
(declare-const capital_expenditures_2018 Real)

(assert (! (= capital_expenditures_2018 1577.0) :named evidence_capital_expenditures_2018))

(assert (! (= computed_capital_expenditures capital_expenditures_2018) :named formula_capital_expenditures))

(assert (!
  (or
    (> (- computed_capital_expenditures 1677.0) 0.5)
    (> (- 1677.0 computed_capital_expenditures) 0.5))
  :named violation_claim_tolerance))

(check-sat)
