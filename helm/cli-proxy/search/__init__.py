"""Docs search for the air-gapped deployment.

search-modal.html asks /convai/api/search-service for results and renders
whatever comes back. On redis.io a hosted service answers; in an air-gapped
cluster nothing does, so the modal opens empty. This package answers with the
same contract, measured against the live service rather than guessed, so the
upstream partial works unmodified.
"""
