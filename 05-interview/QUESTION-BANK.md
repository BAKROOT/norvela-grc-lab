# GRC Interview Question Bank

120 questions. Every one is answerable from work you will have done in this
lab — that is the design. Where a question has a trap, the trap is named.

**How to use this.** Do not read the answers first. Answer aloud, out loud,
into a recorder, then compare. The gap between what you know and what you can
say under mild pressure is the entire problem this bank exists to close.

---

## Category 1 — Risk fundamentals (25)

1. What is the difference between a risk and a finding?
   *Strong answer separates a present-tense control defect from a future loss
   scenario with cause, event and consequence — and says that one risk is
   usually caused by several findings. Weak answers use the words
   interchangeably.*
2. Walk me through how you'd run a risk assessment for a payments platform
   you've never seen before.
3. Inherent vs residual risk — and what sits between them?
4. Risk appetite vs risk tolerance vs risk capacity. Give an example of each
   from a firm you know.
5. Your likelihood scale says "Possible = once in 2–5 years." How did you
   arrive at those boundaries?
6. A business owner wants to accept a critical risk. Walk me through what
   happens next.
7. Who should own a risk — the person who can fix it, or the person who
   suffers if it materialises? Defend your answer.
8. When is a heat map the wrong tool?
9. Explain FAIR to someone who has never heard of it, in 90 seconds.
10. Why does a control reduce vulnerability but not threat event frequency?
    *This is a genuine discriminator. Most candidates get it wrong.*
11. Your Monte Carlo says the P90 annual loss is €3.9M. The CFO says "you
    made that up." What do you say?
12. How many risks should a register for a 340-person company have?
    *There is no right number, but "however many there are" is a bad answer
    and "35–45 well-formed risks, because beyond that nobody reads it and
    below that you've aggregated away the detail" is a good one.*
13. Qualitative or quantitative risk assessment — which and when?
14. What is a key risk indicator, and how is it different from a key
    performance indicator?
15. Give me a KRI for third-party concentration risk.
16. How do you handle a risk that crosses three departments and nobody wants?
17. What is risk velocity and why might it matter more than likelihood?
18. Your register has 23 entries, all scored High or Medium, last updated
    18 months ago. What do you do in your first week?
19. How do you aggregate risk upward for a board without losing meaning?
20. What is a risk that you would deliberately *not* put in the register?
21. Explain the three lines of defence. Now tell me what's wrong with it.
22. Your acting CISO reports to the CTO. Why is that a problem, and what
    would you do if you couldn't change it immediately?
23. How do you set risk appetite when the board has never articulated one?
24. What's the difference between a risk assessment and a gap assessment?
25. Tell me about a risk you were wrong about.

---

## Category 2 — Frameworks and standards (25)

26. ISO 27001 vs ISO 27002 vs ISO 27005 — what does each do?
27. How many controls are in ISO 27001:2022 Annex A and how are they
    organised? *93, across organisational (37), people (8), physical (14),
    technological (34).*
28. Name three controls that are new in the 2022 revision and why they were
    added. *Threat intelligence 5.7, cloud services 5.23, data leakage
    prevention 8.12, configuration management 8.9, information deletion 8.10,
    data masking 8.11, monitoring 8.16 — pick three and explain the gap each
    closed.*
29. What is Amendment 1:2024 and what does it actually require?
    *Climate-change determination in Clause 4.1 and a note in 4.2. No new
    Annex A controls. Candidates who claim new controls reveal they read a
    blog rather than the standard.*
30. What is a Statement of Applicability and why do auditors read the
    exclusions first?
31. Walk me through the ISO 27001 certification lifecycle.
32. Stage 1 vs Stage 2 audit.
33. Major nonconformity vs minor vs observation. Give an example of each.
34. What does Clause 9.3 require, and why is it the most commonly missed?
35. SOC 2 Type I vs Type II.
36. Name the five Trust Services Criteria. Which are optional?
37. A customer asks for your SOC 2. You have ISO 27001. What do you say?
38. What is a bridge letter?
39. NIST CSF 2.0 — what changed from 1.1? *The Govern function was added,
    making six: Govern, Identify, Protect, Detect, Respond, Recover.*
40. When would you use NIST CSF over ISO 27001?
41. PCI DSS: what determines your SAQ type vs needing a RoC?
42. What expands PCI scope unexpectedly? *Answer from the lab: PANs in
    observability logs, and unmasked production data in staging.*
43. What is a compensating control and what makes one acceptable?
44. Explain the difference between a framework, a standard, a regulation and
    a benchmark.
45. How do you map controls across six frameworks without testing six times?
46. What is a control mapping's biggest failure mode?
    *Assuming a mapped control satisfies both at the same depth. ISO's
    "access control" and PCI's requirement 7 are not the same evidence bar.*
47. CIS Controls — what are Implementation Groups for?
48. What is ISO 42001 and who needs it?
49. ISO 27701 — what is it and what does it extend?
50. If you could only implement ten controls at a new company, which ten?

---

## Category 3 — EU regulation (25)

51. What is DORA and who does it apply to?
52. DORA's five pillars. *ICT risk management; incident reporting;
    resilience testing; third-party risk; information sharing.*
53. What is the Register of Information and why does it exist?
54. Walk me through how you'd build one from a messy vendor spreadsheet.
55. What makes a function "critical or important" under DORA?
56. What is a CTPP and how does one get designated?
57. What must a DORA-compliant contract contain?
58. What is threat-led penetration testing and who has to do it?
59. How would you classify a major incident under DORA?
60. What are the DORA reporting deadlines? *Say the structure — initial,
    intermediate, final — and then say you would confirm exact hours against
    Art. 19 and the RTS rather than quote from memory. That is the correct
    professional answer.*
61. What is NIS2 and how is it different from NIS1?
62. Portugal transposed NIS2 how, and when did it take effect?
    *Decreto-Lei 125/2025, published 4 December 2025, in force 3 April 2026,
    establishing the Regime Jurídico da Cibersegurança. CNCS is the lead
    authority, CERT.PT the national CSIRT.*
63. Essential vs important entity — what turns on the distinction?
64. NIS2 imposes management-body liability. What does that mean in practice?
65. Where does DORA displace NIS2 as *lex specialis*, and where doesn't it?
66. GDPR Art. 33 — when does the 72-hour clock start?
    *From awareness, not discovery of full facts. The lab incident is built
    to make you argue this.*
67. When is Art. 34 communication to data subjects required?
68. What is a DPIA and when is it mandatory?
69. Controller vs processor vs joint controller. Give an example where the
    answer is genuinely contested.
70. What transfer mechanisms exist post-Schrems II and what does a TIA involve?
71. Can a part-time DPO who is also company secretary be a conflict under
    Art. 38(6)? Argue it.
72. What is legitimate interest and what does the balancing test require?
73. EU AI Act — what are the risk tiers?
74. What changed with the Digital Omnibus? *Reg. (EU) 2026/1744 moved Annex
    III high-risk obligations to 2 December 2027 and Annex I to 2 August
    2028; Art. 50 transparency applied from 2 August 2026.*
75. A credit-scoring model feeds a partner bank's lending decision. Who is
    the provider and who is the deployer, and does it matter?

---

## Category 4 — Control testing and audit (20)

76. Design effectiveness vs operating effectiveness.
77. How do you choose a sample size?
78. A control operates daily for 12 months. You test 25 instances and find
    one failure. What do you conclude?
79. Rank these from strongest to weakest evidence: a screenshot, a policy
    document, an API export with timestamps, an email confirming a review.
80. How would you test a joiner-mover-leaver control?
81. How would you test that backups work? *"Backups exist" is not the
    control. "Restores succeed within RTO" is.*
82. What makes a test procedure re-performable?
83. What is a walkthrough and when do you do one?
84. You find the same finding as last year, unremediated. What now?
85. The control owner disagrees with your finding. How do you handle it?
86. How do you audit a control that is fully automated?
87. What is continuous control monitoring and what does it require?
88. A vendor gives you their ISO 27001 certificate. What do you ask for next?
    *The SoA and the scope statement — a certificate whose scope excludes
    the service you buy is worthless to you.*
89. How do you test segregation of duties in a company where engineers
    deploy their own code?
90. What is a management representation and why does it not substitute for
    evidence?
91. How do you decide finding severity?
92. Write me a finding. Out loud. Condition, criteria, cause, consequence,
    recommendation.
93. What do you do when there is no evidence because the control has never
    operated?
94. How do you scope an internal audit programme for the year?
95. What's the difference between an internal audit and a self-assessment?

---

## Category 5 — Third party and operational (12)

96. How do you tier vendors?
97. What do you do about a critical vendor that is a two-person company?
98. How do you assess a vendor that refuses to answer your questionnaire?
99. What is concentration risk and why is "multi-cloud" usually the wrong
    answer to it?
100. What belongs in an exit plan, and how do you know it works?
101. How do you map a sub-processor chain you have no visibility into?
102. A vendor was breached. Walk me through your first 24 hours.
103. How do you handle shadow IT discovered through an expense report?
104. What is a right-to-audit clause worth if you never exercise it?
105. How do you assess a vendor's vendor?
106. What questions actually differentiate vendors, versus which are theatre?
107. How would you shorten a 214-question customer security questionnaire
     process from three weeks to two days?

---

## Category 6 — Behavioural and situational (13)

108. Tell me about a time you had to deliver bad news to an executive.
109. The CTO says "the audit is a tax." What do you say to him?
110. How do you get engineering to care about compliance?
111. You have 90 days and a broken programme. What are your first three moves?
112. Tell me about a time you were wrong.
113. How do you prioritise when everything is a regulatory deadline?
114. A board member asks "are we secure?" What do you say?
115. You discover the company has been non-compliant for two years. What now?
116. How do you say no to a business request?
117. Describe a time you changed someone's mind.
118. What's the most useless compliance activity you've seen, and why?
119. Why GRC, after years in offensive and detection work?
     *If this is your path, the answer is genuinely strong: you have seen
     what attackers actually do, so you can tell which controls matter and
     which are paperwork. Most GRC candidates cannot. Lead with it.*
120. What would you do in your first 30 days here?

---

## The four answer patterns that work

**For technical questions — Structure, Specific, Caveat.**
Name the framework or structure, give a specific example from your lab work,
then state the limit of your certainty. "Under DORA the classification runs
against seven criteria — clients affected, data losses, economic impact,
downtime, geographic spread, criticality, reputation. In the settlement-fraud
case I worked, it met the threshold on economic impact and criticality even
before we knew the dwell time. I'd confirm the exact quantitative thresholds
against the RTS before committing a classification in writing."

**For "how would you" questions — Scope, Sequence, Success.**
What you'd scope, in what order, and how you'd know it worked.

**For behavioural — STAR, with the number at the end.**
Situation and task in two sentences. Action in four. Result with a figure.

**When you don't know — say so, then show how you'd find out.**
"I don't know that off the top of my head. I'd check the RTS and the
national competent authority's guidance, because submission windows are set
nationally." This scores *better* than a confident wrong answer with every
interviewer worth working for.
