## mpd 2


### import the directory via curl

**position yourself in directory /apps/staging-api/ and run curl

curl -X POST -F "file=@tests/test_data/thomson.json" \
  http://localhost:8000/api/v1/staging/import/THOMSON/THOMSON


this should result in

{"message":"Data imported for directory THOMSON"}


and sample transition

curl -X POST http://localhost:8000/api/v1/staging/123091211111/transition \
  -H "Content-Type: application/json" \
  -d '{"action": "submit", "created_by": "T123456", "business_justification": "hello"}'



  {
  "record_id": "123091211111",
  "new_status": "pending review",
  "created_by": "T123456",
  "business_justification": "hello",
  "message": "Transition 'submit' applied successfully."
}