# DNA Sequence Analysis API

A REST API for DNA sequence alignment and protein translation, built with FastAPI and Biopython.

Repository: [github.com/Kenrockender/Kalbe-Test](https://github.com/Kenrockender/Kalbe-Test)

## Features

- **Sequence Alignment**: Align DNA sequences to a reference genome and identify variants (SNVs, insertions, deletions)
- **Protein Translation**: Translate DNA sequences to protein in reading frames 1-3
- **Robust Validation**: Comprehensive FASTA format validation with clear error messages
- **Strict Upload Contract**: Exactly one uploaded FASTA file is accepted in the `file` field
- **Well-Tested**: Automated tests cover the API contract, supplied samples, validation edge cases, and bonus analysis endpoint

## Installation

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

## Running with Docker

```bash
docker build -t dna-api .
docker run --rm -p 8000:8000 dna-api
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### POST /api/align

Align a DNA sequence to the reference and report variants.

**Input**: FASTA file (multipart/form-data)

**Example**:
```bash
curl -X POST "http://localhost:8000/api/align" \
  -F "file=@patient_01.fasta"
```

**Response**:
```json
{
  "sequence_id": "patient_01",
  "reference_id": "REF_001",
  "alignment": {
    "score": 300.0,
    "identity": 1.0,
    "reference_aligned": "ATGAGTTCG...",
    "query_aligned": "ATGAGTTCG..."
  },
  "variants": []
}
```

### POST /api/translate

Translate DNA sequence to protein.

**Input**: 
- `file`: FASTA file (multipart/form-data)
- `frame`: Reading frame 1, 2, or 3 (form field, default: 1)

**Example**:
```bash
curl -X POST "http://localhost:8000/api/translate" \
  -F "file=@patient_01.fasta" \
  -F "frame=1"
```

**Response**:
```json
{
  "sequence_id": "patient_01",
  "frame": 1,
  "protein": "MSSSVPLLYVSRVGTSOQLFSLFTKFT...",
  "length": 99,
  "has_stop_codon": false
}
```

## FASTA Requirements

- Exactly one uploaded file in the multipart `file` field, containing one FASTA record
- 1-1000 nucleotides
- Valid characters: A, C, G, T, N (case-insensitive)
- Standard FASTA format with header line starting with `>`

## Running Tests

```bash
# Run all tests (reproduce the results below)
pytest -v

# Run a specific test file
pytest tests/test_align_api.py -v

# Run with coverage
pytest --cov=app --cov-report=html
```

### Automated Test Results

The full test suite output (139 tests, all passing):

```
===================================== test session starts ======================================
platform win32 -- Python 3.11.9, pytest-8.3.4, pluggy-1.7.0
cachedir: .pytest_cache
rootdir: C:\Users\kenro\Downloads\dna-api-clean

tests/test_align_api.py::TestAlignEndpoint::test_patient_01_perfect_match PASSED          [  0%]
tests/test_align_api.py::TestAlignEndpoint::test_patient_02_three_snvs PASSED             [  1%]
tests/test_align_api.py::TestAlignEndpoint::test_patient_03_two_deletions PASSED          [  2%]
tests/test_align_api.py::TestAlignEndpoint::test_patient_04_n_handling PASSED            [  2%]
tests/test_align_api.py::TestAlignEndpoint::test_patient_05_two_insertions PASSED        [  3%]
tests/test_align_api.py::TestAlignedSequencesInvariant::test_patient_01_invariant PASSED  [  4%]
tests/test_align_api.py::TestAlignedSequencesInvariant::test_patient_02_invariant PASSED  [  5%]
tests/test_align_api.py::TestAlignDeterminism::test_same_input_same_output PASSED         [  5%]
tests/test_align_api.py::TestAlignErrors::test_missing_file PASSED                        [  6%]
tests/test_align_api.py::TestAlignErrors::test_invalid_fasta_multiple_records PASSED      [  7%]
tests/test_align_api.py::TestAlignErrors::test_invalid_fasta_no_header PASSED            [  7%]
tests/test_align_api.py::TestAlignErrors::test_sequence_too_long PASSED                   [  8%]
tests/test_align_api.py::TestAlignErrors::test_invalid_characters PASSED                  [  9%]
tests/test_fasta.py::TestValidFasta::test_single_line_sequence PASSED                    [ 10%]
tests/test_fasta.py::TestValidFasta::test_multiline_sequence PASSED                      [ 10%]
tests/test_fasta.py::TestValidFasta::test_lowercase_to_uppercase PASSED                  [ 11%]
tests/test_fasta.py::TestValidFasta::test_mixed_case PASSED                              [ 12%]
tests/test_fasta.py::TestValidFasta::test_blank_lines_ignored PASSED                     [ 12%]
tests/test_fasta.py::TestValidFasta::test_crlf_line_endings PASSED                       [ 13%]
tests/test_fasta.py::TestValidFasta::test_cr_line_endings PASSED                         [ 14%]
tests/test_fasta.py::TestValidFasta::test_utf8_bom PASSED                                [ 15%]
tests/test_fasta.py::TestValidFasta::test_header_with_description PASSED                 [ 15%]
tests/test_fasta.py::TestValidFasta::test_n_nucleotides PASSED                           [ 16%]
tests/test_fasta.py::TestValidFasta::test_all_n_sequence PASSED                          [ 17%]
tests/test_fasta.py::TestValidFasta::test_leading_trailing_whitespace_on_lines PASSED    [ 17%]
tests/test_fasta.py::TestValidFasta::test_max_length_1000 PASSED                         [ 18%]
tests/test_fasta.py::TestInvalidFasta::test_empty_file PASSED                            [ 19%]
tests/test_fasta.py::TestInvalidFasta::test_whitespace_only_file PASSED                  [ 20%]
tests/test_fasta.py::TestInvalidFasta::test_no_header PASSED                             [ 20%]
tests/test_fasta.py::TestInvalidFasta::test_empty_header PASSED                          [ 21%]
tests/test_fasta.py::TestInvalidFasta::test_header_only_whitespace PASSED                [ 22%]
tests/test_fasta.py::TestInvalidFasta::test_empty_sequence PASSED                        [ 23%]
tests/test_fasta.py::TestInvalidFasta::test_sequence_only_whitespace PASSED              [ 23%]
tests/test_fasta.py::TestInvalidFasta::test_multiple_records PASSED                      [ 24%]
tests/test_fasta.py::TestInvalidFasta::test_text_before_header PASSED                    [ 25%]
tests/test_fasta.py::TestInvalidFasta::test_invalid_character_u PASSED                   [ 25%]
tests/test_fasta.py::TestInvalidFasta::test_invalid_character_r PASSED                   [ 26%]
tests/test_fasta.py::TestInvalidFasta::test_invalid_character_dash PASSED                [ 27%]
tests/test_fasta.py::TestInvalidFasta::test_invalid_character_asterisk PASSED            [ 28%]
tests/test_fasta.py::TestInvalidFasta::test_invalid_character_digit PASSED              [ 28%]
tests/test_fasta.py::TestInvalidFasta::test_embedded_whitespace_space PASSED             [ 29%]
tests/test_fasta.py::TestInvalidFasta::test_embedded_whitespace_tab PASSED               [ 30%]
tests/test_fasta.py::TestInvalidFasta::test_length_1001_rejected PASSED                  [ 30%]
tests/test_fasta.py::TestInvalidFasta::test_length_2000_rejected PASSED                  [ 31%]
tests/test_fasta.py::TestInvalidFasta::test_invalid_encoding PASSED                      [ 32%]
tests/test_requirement_coverage.py::test_translate_accepts_every_supplied_patient_file[patient_01] PASSED [ 33%]
tests/test_requirement_coverage.py::test_translate_accepts_every_supplied_patient_file[patient_02] PASSED [ 33%]
tests/test_requirement_coverage.py::test_translate_accepts_every_supplied_patient_file[patient_03] PASSED [ 34%]
tests/test_requirement_coverage.py::test_translate_accepts_every_supplied_patient_file[patient_04] PASSED [ 35%]
tests/test_requirement_coverage.py::test_translate_accepts_every_supplied_patient_file[patient_05] PASSED [ 35%]
tests/test_requirement_coverage.py::test_endpoints_normalize_lowercase_multiline_fasta[/api/align] PASSED [ 36%]
tests/test_requirement_coverage.py::test_endpoints_normalize_lowercase_multiline_fasta[/api/translate] PASSED [ 37%]
tests/test_requirement_coverage.py::test_endpoints_reject_malformed_fasta[ATGC-no_header-/api/align] PASSED [ 38%]
tests/test_requirement_coverage.py::test_endpoints_reject_malformed_fasta[ATGC-no_header-/api/translate] PASSED [ 38%]
tests/test_requirement_coverage.py::test_endpoints_reject_malformed_fasta[>first\nATG\n>second\nATG-multiple_records-/api/align] PASSED [ 39%]
tests/test_requirement_coverage.py::test_endpoints_reject_malformed_fasta[>first\nATG\n>second\nATG-multiple_records-/api/translate] PASSED [ 40%]
tests/test_requirement_coverage.py::test_endpoints_enforce_sequence_length_limit[/api/align] PASSED [ 41%]
tests/test_requirement_coverage.py::test_endpoints_enforce_sequence_length_limit[/api/translate] PASSED [ 41%]
tests/test_requirement_coverage.py::test_endpoints_reject_multiple_uploaded_files[/api/align] PASSED [ 42%]
tests/test_requirement_coverage.py::test_endpoints_reject_multiple_uploaded_files[/api/translate] PASSED [ 43%]
tests/test_requirement_coverage.py::test_endpoints_reject_multiple_uploaded_files[/api/analyze] PASSED [ 43%]
tests/test_requirement_coverage.py::test_translate_endpoint_handles_n_codons_and_incomplete_final_codon PASSED [ 44%]
tests/test_requirement_coverage.py::test_analyze_endpoint_annotates_patient_02_effects PASSED [ 45%]
tests/test_requirement_coverage.py::test_analyze_endpoint_classifies_patient_03_indels PASSED [ 46%]
tests/test_translate_api.py::TestTranslateEndpoint::test_patient_02_frame_1 PASSED        [ 46%]
tests/test_translate_api.py::TestTranslateEndpoint::test_frame_1_explicit PASSED          [ 47%]
tests/test_translate_api.py::TestTranslateEndpoint::test_frame_2 PASSED                   [ 48%]
tests/test_translate_api.py::TestTranslateEndpoint::test_frame_3 PASSED                   [ 48%]
tests/test_translate_api.py::TestTranslateEndpoint::test_n_codons_become_x PASSED        [ 49%]
tests/test_translate_api.py::TestTranslateEndpoint::test_has_stop_codon_true PASSED      [ 50%]
tests/test_translate_api.py::TestTranslateEndpoint::test_incomplete_codon_ignored PASSED [ 51%]
tests/test_translate_api.py::TestTranslateFrameValidation::test_invalid_frame_0 PASSED    [ 51%]
tests/test_translate_api.py::TestTranslateFrameValidation::test_invalid_frame_4 PASSED   [ 52%]
tests/test_translate_api.py::TestTranslateFrameValidation::test_invalid_frame_abc PASSED  [ 53%]
tests/test_translate_api.py::TestTranslateFrameValidation::test_invalid_frame_float PASSED [ 53%]
tests/test_translate_api.py::TestTranslateFrameValidation::test_omitted_frame_uses_default PASSED [ 54%]
tests/test_translate_api.py::TestTranslateErrors::test_missing_file PASSED               [ 55%]
tests/test_translate_api.py::TestTranslateErrors::test_invalid_fasta_multiple_records PASSED [ 56%]
tests/test_translate_api.py::TestTranslateErrors::test_sequence_too_long PASSED          [ 56%]
tests/test_translate_api.py::TestTranslateErrors::test_invalid_characters PASSED         [ 57%]
tests/test_translate_api.py::TestTranslateDeterminism::test_same_input_same_output PASSED [ 58%]
tests/test_translation.py::TestTranslationFrames::test_frame_1 PASSED                    [ 58%]
tests/test_translation.py::TestTranslationFrames::test_frame_2 PASSED                    [ 59%]
tests/test_translation.py::TestTranslationFrames::test_frame_3 PASSED                    [ 60%]
tests/test_translation.py::TestTranslationFrames::test_different_frames_different_proteins PASSED [ 61%]
tests/test_translation.py::TestIncompleteCodons::test_trailing_1_nucleotide_ignored PASSED [ 61%]
tests/test_translation.py::TestIncompleteCodons::test_trailing_2_nucleotides_ignored PASSED [ 62%]
tests/test_translation.py::TestIncompleteCodons::test_no_complete_codon_frame_1 PASSED   [ 63%]
tests/test_translation.py::TestIncompleteCodons::test_no_complete_codon_frame_2 PASSED   [ 64%]
tests/test_translation.py::TestIncompleteCodons::test_no_complete_codon_frame_3 PASSED   [ 64%]
tests/test_translation.py::TestStopCodons::test_stop_at_taa PASSED                       [ 65%]
tests/test_translation.py::TestStopCodons::test_stop_at_tag PASSED                       [ 66%]
tests/test_translation.py::TestStopCodons::test_stop_at_tga PASSED                       [ 66%]
tests/test_translation.py::TestStopCodons::test_stop_not_in_output PASSED               [ 67%]
tests/test_translation.py::TestStopCodons::test_no_stop_codon PASSED                     [ 68%]
tests/test_translation.py::TestStopCodons::test_stop_as_first_codon PASSED               [ 69%]
tests/test_translation.py::TestNNucleotides::test_n_in_codon_becomes_x PASSED            [ 69%]
tests/test_translation.py::TestNNucleotides::test_all_n_codon PASSED                     [ 70%]
tests/test_translation.py::TestNNucleotides::test_n_first_position PASSED                [ 71%]
tests/test_translation.py::TestNNucleotides::test_n_second_position PASSED               [ 71%]
tests/test_translation.py::TestNNucleotides::test_n_third_position PASSED                [ 72%]
tests/test_translation.py::TestNNucleotides::test_ggn_becomes_x_not_g PASSED            [ 73%]
tests/test_translation.py::TestNNucleotides::test_multiple_n_codons PASSED               [ 74%]
tests/test_translation.py::TestNNucleotides::test_stop_with_n_not_a_stop PASSED         [ 74%]
tests/test_translation.py::TestNNucleotides::test_tan_not_stop PASSED                    [ 75%]
tests/test_translation.py::TestNNucleotides::test_tgn_not_stop PASSED                    [ 76%]
tests/test_translation.py::TestRealSequences::test_standard_protein PASSED               [ 76%]
tests/test_translation.py::TestRealSequences::test_with_trailing_and_stop PASSED        [ 77%]
tests/test_translation.py::TestEdgeCases::test_empty_sequence PASSED                     [ 78%]
tests/test_translation.py::TestEdgeCases::test_single_nucleotide PASSED                  [ 79%]
tests/test_translation.py::TestEdgeCases::test_exactly_three_nucleotides PASSED          [ 79%]
tests/test_translation.py::TestEdgeCases::test_invalid_frame_raises PASSED               [ 80%]
tests/test_variants.py::TestVariantExtraction::test_single_snv PASSED                    [ 81%]
tests/test_variants.py::TestVariantExtraction::test_multiple_snvs PASSED                 [ 82%]
tests/test_variants.py::TestVariantExtraction::test_insertion_at_position_0 PASSED        [ 82%]
tests/test_variants.py::TestVariantExtraction::test_insertion_mid_sequence PASSED        [ 83%]
tests/test_variants.py::TestVariantExtraction::test_deletion_at_position_1 PASSED        [ 84%]
tests/test_variants.py::TestVariantExtraction::test_deletion_mid_sequence PASSED         [ 84%]
tests/test_variants.py::TestVariantExtraction::test_multi_base_indel_grouped PASSED      [ 85%]
tests/test_variants.py::TestVariantExtraction::test_two_separate_indels PASSED           [ 86%]
tests/test_variants.py::TestVariantExtraction::test_adjacent_snv_and_indel PASSED        [ 87%]
tests/test_variants.py::TestVariantExtraction::test_n_is_not_snv PASSED                   [ 87%]
tests/test_variants.py::TestVariantExtraction::test_n_vs_n_not_snv PASSED                [ 88%]
tests/test_variants.py::TestVariantExtraction::test_n_vs_different_base_not_snv PASSED  [ 89%]
tests/test_variants.py::TestVariantExtraction::test_event_ordering PASSED                [ 89%]
tests/test_variants.py::TestIdentityCalculation::test_perfect_identity PASSED           [ 90%]
tests/test_variants.py::TestIdentityCalculation::test_one_mismatch PASSED                [ 91%]
tests/test_variants.py::TestIdentityCalculation::test_gap_in_denominator PASSED          [ 92%]
tests/test_variants.py::TestIdentityCalculation::test_n_in_denominator_no_match PASSED  [ 92%]
tests/test_variants.py::TestIdentityCalculation::test_n_vs_base_no_match PASSED          [ 93%]
tests/test_variants.py::TestIdentityCalculation::test_gap_vs_base_no_match PASSED        [ 94%]
tests/test_variants.py::TestIdentityCalculation::test_all_gaps_zero_identity PASSED      [ 94%]
tests/test_variants.py::TestIdentityCalculation::test_empty_sequences PASSED             [ 95%]
tests/test_variants.py::TestFullAlignment::test_perfect_match PASSED                     [ 96%]
tests/test_variants.py::TestFullAlignment::test_single_mismatch PASSED                   [ 97%]
tests/test_variants.py::TestFullAlignment::test_alignment_with_gap PASSED                [ 97%]
tests/test_variants.py::TestFullAlignment::test_n_handling PASSED                        [ 98%]
tests/test_variants.py::TestFullAlignment::test_aligned_sequences_correct_length PASSED  [ 99%]
tests/test_variants.py::TestFullAlignment::test_deterministic_output PASSED              [100%]

================================ 139 passed, 1 warning in 2.66s ================================
```

**Test Breakdown**:
- ✅ 32 FASTA validation tests — [`tests/test_fasta.py`](tests/test_fasta.py)
- ✅ 31 translation tests (frames, stops, N handling) — [`tests/test_translation.py`](tests/test_translation.py)
- ✅ 27 alignment and variant extraction tests — [`tests/test_variants.py`](tests/test_variants.py)
- ✅ 13 align endpoint tests (all patient files) — [`tests/test_align_api.py`](tests/test_align_api.py)
- ✅ 17 translate endpoint tests — [`tests/test_translate_api.py`](tests/test_translate_api.py)
- ✅ 16 API-level requirement regression tests, including every supplied patient file and `/api/analyze` — [`tests/test_requirement_coverage.py`](tests/test_requirement_coverage.py)

All edge cases covered including N nucleotides, incomplete codons, stop codons, gaps, and error conditions.

## Alignment Scoring

- **Match**: +1
- **Mismatch**: -1
- **Gap (open and extend)**: -2 each
- **N vs any base**: 0

## Identity Calculation

```
Identity = (matching ACGT bases) / (total alignment columns)
```

Gap columns and N columns count in the denominator but never as matches.

## Coordinate System

All positions are **1-based**:
- **SNV**: Position is the reference position
- **Insertion**: Position is the preceding reference base (0 = before first base)
- **Deletion**: Position is the first deleted base

## Translation Rules

- Frame 1/2/3 = start at nucleotide 1/2/3 (1-based)
- Only complete codons translated (trailing 1-2 nt ignored)
- Any codon containing N becomes X
- Translation stops at first unambiguous stop codon (TAA, TAG, TGA)
- Stop codon (*) not included in output

## Error Handling

All validation errors return HTTP 422 with consistent JSON format:

```json
{
  "error": "error_code",
  "detail": "Human-readable error message"
}
```

Common error codes:
- `no_header`: Missing FASTA header
- `multiple_records`: More than one sequence in file
- `sequence_too_long`: Sequence exceeds 1000 nt
- `invalid_characters`: Non-ACGTN characters found
- `invalid_frame`: Frame not 1, 2, or 3
- `multiple_files`: More than one uploaded file was provided

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration constants
│   ├── errors.py            # Custom exceptions
│   ├── schemas.py           # Pydantic response models
│   ├── routers/             # API endpoints
│   │   ├── __init__.py
│   │   ├── align.py         # /api/align endpoint
│   │   ├── analyze.py       # /api/analyze endpoint
│   │   └── translate.py     # /api/translate endpoint
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── fasta.py         # FASTA parsing & validation
│   │   ├── reference.py     # Reference loading
│   │   ├── alignment.py     # Sequence alignment
│   │   ├── translation.py   # DNA translation
│   │   ├── effects.py      # Variant effect annotation
│   │   └── upload.py        # Multipart upload handling
│   └── data/
│       └── reference.fasta  # Reference sequence
├── static/                  # Browser interface
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── samples/             # Sample FASTA files
├── tests/                   # Comprehensive test suite (139 tests)
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Design Decisions

### Why FastAPI?
- Automatic API documentation via OpenAPI/Swagger
- Pydantic for data validation
- High performance with async support
- Easy to test with TestClient

### Why Biopython?
- Industry-standard bioinformatics library
- Well-tested PairwiseAligner implementation
- Reliable genetic code tables
- Saves development time on complex algorithms

### Architecture
- **Routers**: Handle HTTP requests/responses
- **Services**: Contain business logic (testable without HTTP)
- **Schemas**: Define API contracts with Pydantic

This separation allows comprehensive unit testing of business logic independent of the API layer.

## Assumptions

1. **Reading frames**: Frame 1/2/3 means starting at nucleotide position 1/2/3 of the input sequence (no start codon search)
2. **Stop codons**: Translation stops at first TAA/TAG/TGA; * is excluded from output
3. **Linear gap scoring**: Both gap open and gap extend penalties are -2
4. **End gaps**: Penalized (contribute to score)
5. **Tie-breaking**: When multiple optimal alignments exist, Biopython returns them in a deterministic order; we take the first

## Limitations

1. **N regions**: Indel placement within or adjacent to N runs is arbitrary
2. **Nearby variants**: Effect annotation (bonus feature) evaluates each variant independently
3. **Biopython dependency**: Core algorithms use Biopython rather than hand-written implementations

## Development

Built with clean git history showing incremental development:
1. Project skeleton and FASTA validation
2. Translation service
3. Alignment and variant extraction
4. API endpoints with error handling
5. Comprehensive test suite

All code follows Python best practices with type hints, docstrings, and clear separation of concerns.

## License

MIT License - Free for educational and commercial use.
