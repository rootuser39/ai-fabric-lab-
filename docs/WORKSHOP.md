# Workshop 01 — Why average load can hide packet loss

Audience: Python beginners, network engineers and developers learning AI
infrastructure. Requires a Python interpreter, not a GPU. Suggested length:
45 minutes. This is a prepared lesson, not a record of an event already held.

## 1. Predict — 5 minutes

Eight senders each send one packet per 16 us. One packet takes 1 us to transmit.
The average offered rate is half the output capacity. Can packets still drop?
Write a prediction before running code. Define the missing assumption.

## 2. Observe — 10 minutes

Run `python -m fabriclab suite`. Compare synchronized and staggered inputs.
Inspect dropped packets, per-sender deliveries, p99 and completion status.
Explain why half the traffic can drop despite the modest long-run average.

## 3. Change one variable — 10 minutes

Run `python -m fabriclab incast --capacity 8`. Predict before execution.
Explain why eliminating loss can increase the delivered-packet p99. Then run
`python -m fabriclab incast --staggered --interval-us 4`. Why is staggering now
insufficient? Keep all other settings unchanged.

## 4. Challenge the model — 10 minutes

Identify the sender-order bias, absent retransmissions and absent propagation.
Explain why the simulator is not evidence of a real RDMA throughput advantage.
Describe measurements that would test the idea on hardware without claiming
the real system behaves like this one.

## 5. Publish a reproducible finding — 10 minutes

Submit a hypothesis, command, output excerpt, explanation and limitation.
Use this rubric: correct prediction reasoning (2), reproducibility (2), metric
interpretation (2), limitations (2), explanation someone else can follow (2).
Keep the original prediction, even when wrong. Do not count an AI-generated
explanation as a learner's demonstrated understanding.
