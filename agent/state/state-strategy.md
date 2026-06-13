# State Strategy

The MVP is stateless between commands. In-memory entries and overlap candidates
exist only for the duration of one process.

Generated catalogs are outputs, not resumable runtime checkpoints. The public
repository must not contain real run state, session snapshots, pending
approvals, or tool-call histories.
