# Combined wallpaper collection

- **34 finished masters:** the current original fourteen and both approved batches of ten from Century.
- **10 queued concepts:** 101–110, now registered in `backlog.json`; no images generated yet.
- **80 archived rejections:** retained in the original Century register, not eligible for automatic revival.

`catalog.json` is the combined index. Original IDs use `oNN`; Century IDs use
`cNNN`. Original and Century numbering intentionally remain distinct.

[Ranked review](../../concepts/century/ranking/index.html) shows all 34, with
individual reasoning and a proposed cutoff after rank 22. The recommendation
is stored separately in `quality-ranking.json`; it does not change membership.
The user authorized the twelve redesigns. They are now complete as new review versions; collection membership remains unchanged. [Compare before / after](../../concepts/century/quality-redesign/index.html).

```sh
./finalized              # All 34, in proposed ranking order
./finalized truth-lamp   # Start at a named sheet
./finalized --list
./century                # The 20 retained Century sheets, in original ID order
```

The collection uses symbolic links to current masters. The quality pass regenerated twelve sheets in both formats and preserved their previous versions. It did not install them on the desktop.
In `./finalized`, numeric selection is the ranking position; use a name to avoid
confusing it with the original series number.

The ranking is the editorial baseline before the twelve redesigns, not a fresh score for the revised artwork. The redesign pass audited both formats and documented the scope and mechanical limitations in [QUALITY-REDESIGN.md](QUALITY-REDESIGN.md). Existing acceptance is retained; being placed below the
proposed release threshold means a further redesign recommendation, not a
retroactive rejection.

Rebuild the gallery after changes with `python tools/century/ranking_gallery.py`.
Revisit the ranking whenever a referenced master SHA changes; re-exporting the
gallery alone must not be treated as a fresh quality assessment.

All 34 now share Field Notes and a separate, smaller Omarchy signature, with both native formats audited. [Format revision](FORMAT-UNIFICATION.md) · [Before / after](../../concepts/century/format-unification/index.html). The master hashes reflect this format revision; the ranking order still describes the earlier editorial baseline.
