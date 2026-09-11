# Community execution roadmap

## Purpose

Help developers without expensive infrastructure build useful intuition about
AI communication, then connect that intuition to reproducible NVIDIA stack
measurements. The educational contribution is explanation and verification,
not claiming a new proprietary networking technology.

## Current evidence

Runnable synthetic experiments, unit tests, a constrained NCCL log reader and
a prepared workshop. No external adoption, delivered mentoring, audience size,
NVIDIA validation or program acceptance is claimed.

## Proposed six-week sequence

| Week | Deliverable | Completion evidence |
|---|---|---|
| 1 | Review and teach the incast experiment | Published explanation and exact reproduction commands |
| 2 | Invite external reproductions | Voluntary reports, including failures; actual counts only |
| 3 | Run a beginner workshop | Event link, consented feedback and anonymized learning outcomes |
| 4 | Add a hardware-backed NCCL baseline if access permits | Sanitized run manifest and raw results |
| 5 | Write one measured troubleshooting case | Observation, alternatives tested, evidence and limitation |
| 6 | Improve the lesson from feedback | Linked revisions and issues resolved |

If hardware is unavailable, explicitly keep that milestone pending. Do not
replace measurements with synthetic numbers presented as real results.

## What to track

Independent successful reproductions; failed reproductions resolved; learner
explanations before/after the workshop; externally contributed improvements;
repeat participants; useful public answers. Stars are secondary to whether
someone can understand, run and apply the work.

## Guardrails

Contributors use approved lab resources only. No production fault injection,
employer configurations, private designs, access tokens or sensitive logs.
Opening this repository publicly does not authorize reuse of unrelated private
projects. AI-assisted contributions must be identified and reviewed.
