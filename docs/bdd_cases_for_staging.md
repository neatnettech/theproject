# Test Cases for Staging

## Market-Driven Changes (System-Suggested Updates)

These changes come directly from Market Directory File and reflect the market’s latest information. 

### New Records from the Market
  
#### Test Case ID: TC-001

**Scenario**
Approve a new record that exists in the file but not in the database

**Preconditions**
File contains a new record; no existing DB entry

**Expected Result**
The new record is inserted into the database.

**Acceptance Criteria (BDD)**
`Given` a new record is found in the file that is not already in the database,
`When` the user approves the new record in the staging area,
`Then` the new record is added to the database and marked as active.

---

#### Test Case ID: TC-002

**Scenario**
Reject a new record that exists in the file but not in the database

**Preconditions**
Same as TC-001

**Expected Result**
The record is added, marked as inactive and an override prevents future automatic insertion.

**Acceptance Criteria (BDD)**
`Given` a new record is found in the file that is not already in the database,
`When` the user rejects the new record in the staging area,
`Then` the record in the database is added to the database and marked as inactive, with a flag that indicates a manual override.

---

#### Test Case ID: TC-003

**Scenario**
Activate a new record that matches a previously deactivated record

**Preconditions**
Previously deleted record exists in DB with inactive flag

**Expected Result**
System reactivates the existing record instead of creating a duplicate.

**Acceptance Criteria (BDD)**
`Given` a record has been deactivated (its active flag set to inactive) and a new record is added that matches the deactivated record,
`When` the user accepts the new record in the staging area,
`Then` the system should check for the deactivated record and reactivate it, setting the active flag back to active.

---

#### Test Case ID: TC-004

**Scenario**
Reject a new record that matches a previously deactivated record

**Preconditions**
Previously deleted record exists in DB with inactive flag

**Expected Result**
The record is not activated, and an override prevents future automatic insertion.

**Acceptance Criteria (BDD)**
`Given` a record has been deactivated (its active flag set to inactive) and a new record is added that matches the deactivated record,
`When` the user rejects the new record in the staging area,
`Then` the system should check for the deactivated record and reactivate it, setting a flag that indicates a manual override.

---
### Updates from the Market (No Manual Overrides in DB)

#### Test Case ID: TC-005

**Scenario**
Approve an update for a record that matches the market with no manual changes

**Preconditions**
Record exists in DB but has no prior manual modifications

**Expected Result**
Record is updated in the database.

**Acceptance Criteria (BDD)**
`Given` an existing record in the database matches the updated data in the file,
`When` the user approves the update,
`Then` the record in the database is updated with the new data from the file.

---

#### Test Case ID: TC-006

**Scenario**
Reject an update for a record that matches the market with no manual changes

**Preconditions**
Same as TC-005

**Expected Result**
The record is not updated, and an override prevents future auto-updates.

**Acceptance Criteria (BDD)**
`Given` an existing record in the database matches the updated data in the file,
`When` the user rejects the update,
`Then` the system should retain the original data in the database and prevent future automatic updates for that record.

Here is the next batch of test cases in **plain Markdown format**, following your specified structure:

---

#### Test Case ID: TC-007

**Scenario**  
Approve a deletion from the file

**Preconditions**  
Record exists in DB but is marked for deletion in File

**Expected Result**  
Record is deactivated in the database (active/inactive flag set to inactive).

**Acceptance Criteria (BDD)**  
`Given` that a record in the system is marked for deletion in the file,  
`When` the user approves the deletion,  
`Then` the record should remain in the database but have its active flag set to inactive, and it should no longer appear as active in the system.

---

#### Test Case ID: TC-008

**Scenario**  
Reject a deletion from the file

**Preconditions**  
Same as TC-007

**Expected Result**  
Record remains active in the database, and override prevents future automatic deletions.

**Acceptance Criteria (BDD)**  
`Given` that a record in the system is marked for deletion in the file,  
`When` the user rejects the deletion,  
`Then` the record should remain in the database but have its active flag set to active, setting a flag that indicates a manual override.

---
### Market-Driven Changes (User Overrides & Conflict Resolution)

These records have been previously modified manually, so changes from Market Directory Files need careful handling.

#### Test Case ID: TC-009

**Scenario**  
Approve an update for a record that exists in DB and has manual overrides

**Preconditions**  
Record exists in DB and has manual overrides

**Expected Result**  
System updates the record but logs the change history.

**Acceptance Criteria (BDD)**  
`Given` a record has been manually modified,  
`When` the system detects an update for that record from the file,  
`Then` the user should be able to approve the update, which will overwrite the manual change with the new market data.

---

#### Test Case ID: TC-010

**Scenario**  
Modify an update for a record that exists in DB and has manual overrides

**Preconditions**  
Same as TC-009

**Expected Result**  
Record is updated with manual modifications, keeping audit history.

---

#### Test Case ID: TC-011

**Scenario**  
Reject an update for a record that exists in DB and has manual overrides

**Preconditions**  
Same as TC-009

**Expected Result**  
Record remains unchanged, and override prevents future automatic updates.

**Acceptance Criteria (BDD)**  
`Given` a record has been manually modified,  
`When` the system detects an update for that record from the file,  
`Then` the user should be able to reject the update, which will preserve the manual change and prevent the system from overwriting it.

---
---
##### TC-011. Case Scenario Analysis

###### Opt 1. 
System compares two Market files to create the deltas, the Manual Overrides are only considered in a second phase of the process; the user only is presented with changes if the Market file changes. i.e: 

+ User creates a manual override to a record in March 2024. 
+ Market file from April 2024 does not contain any changes to that record compared to the March 2024 file. 
+ The system does not flag a change for this record. 
+ The user is not involved in the process. 
+ The system does not find any difference in tha record until September 2024. 
+ Record contains and update from August to September 2024. 
+ The system registers the delta. In a second step, checks that the record has a ‘Manual Override’ flag. 
+ The user is presented with the changes for approval.

###### Opt 2. 
System compares the Market data to the data base. The Manual Overrides get flagged every month until the Market aligns with the override or the User creates additional changes to align - or time based flag gets set?. i.e:

+ User creates a manual override to a record in March 2024. 
+ Market file from April 2024 does not contain any changes to that record compared to the March 2024 file. 
+ Market data differs from the data base record which has a manual override.
+ User is presented with and update proposal in the staging area in April 2024
+ User rejects the update
+ A flag is set to not propose this change in 6 months
+ A change from the market happens in June 2024 but the change does not align with the manual override
+ The user does not get notified about the change until October 2024
+ User approves the market change
+ The data was outdated for several months

Market data at the time of the Manual Override needs to be stored with the record and compared against 
---
---

#### Test Case ID: TC-012

**Scenario**  
Automatic update for a record that exists in DB and has manual overrides, and the update matches the manual overrides

**Preconditions**  
Same as TC-009

**Expected Result**  
Override flag is automatically updated in the database.

**Acceptance Criteria (BDD)**  
`Given` a record has been manually modified,  
`When` the system detects an update for that record from the file which matches the manual changes,  
`Then` system sets the manual override flag to `None`, and user gets notified about the data reconciliation.

---

## Manual-Driven Changes

### User Creates a New Record

#### Test Case ID: USR-01
**Scenario**: User creates a new record manually  
**Preconditions**: The record does not exist in the database (active or inactive)  
**Expected Result**: The system saves the record as user-generated, preventing automatic overwrites by market updates  
**Acceptance Criteria (BDD)**:  
`Given` the record does not exist,  
`When` the user creates a new record,  
`Then` the system saves it as user-generated and prevents automatic overwrites  

---

#### Test Case ID: USR-02
**Scenario**: User tries to create a record that already exists as inactive  
**Preconditions**: A record with the same details exists but is inactive  
**Expected Result**: The system prompts the user to reactivate the existing record instead of creating a duplicate  
**Acceptance Criteria (BDD)**:  
`Given` the record exists but is inactive,  
`When` the user tries to create a new one,  
`Then` the system prompts them to reactivate instead  

---

#### Test Case ID: USR-03
**Scenario**: User creates a new record, and later a market update for the same entity arrives  
**Preconditions**: The user manually created a record before the market update arrived  
**Expected Result**: The system flags the record as conflicting and asks for user review  
**Acceptance Criteria (BDD)**:  
`Given` a record exists as user-generated,  
`When` a market update arrives for the same entity,  
`Then` the system marks it as a conflict and requests user intervention  

---
### User Modifies an Existing Record (Manual Override)

#### Test Case ID: USR-04
**Scenario**: User manually edits an existing record  
**Preconditions**: The record exists in an active state  
**Expected Result**: The system marks the record as manually override, blocking automatic updates from market files  
**Acceptance Criteria (BDD)**:  
`Given` a record exists,  
`When` the user modifies it,  
`Then` the system marks it as manually override and prevents automatic market updates  

---

#### Test Case ID: USR-05
**Scenario**: A market update arrives for a manually modified record  
**Preconditions**: The record has been manually modified in the past  
**Expected Result**: The system alerts the user and presents a side-by-side comparison of manual vs. market data  
**Acceptance Criteria (BDD)**:  
`Given` a record was manually modified,  
`When` a market update arrives,  
`Then` the system prompts the user for review  

---

#### Test Case ID: USR-06
**Scenario**: User overrides a previous manual change with a new update  
**Preconditions**: A record already has a manual override  
**Expected Result**: The system logs the new change and allows updates based on the most recent manual input  
**Acceptance Criteria (BDD)**:  
`Given` a record was already modified by a user,  
`When` another modification is made,  
`Then` the system updates the override log  

---

#### Test Case ID: USR-07
**Scenario**: User reverts a manual change and wants market updates to resume  
**Preconditions**: The record has been modified manually  
**Expected Result**: The system removes the manual override flag and allows market updates again  
**Acceptance Criteria (BDD)**:  
`Given` a record was previously modified,  
`When` the user removes the override,  
`Then` the system restores market updates  

---
### User Deletes a Record (Soft Delete / Deactivation)

#### Test Case ID: USR-08
**Scenario**: User deletes a record  
**Preconditions**: The record exists in an active state  
**Expected Result**: The system deactivates the record instead of removing it  
**Acceptance Criteria (BDD)**:  
`Given` a record is active,  
`When` the user deletes it,  
`Then` the system sets the active flag to ‘inactive’ instead of deleting the data  

---

#### Test Case ID: USR-09
**Scenario**: User tries to delete a record but a market update is pending  
**Preconditions**: A market update for the record exists in staging  
**Expected Result**: The system warns the user and requests confirmation before deactivating  
**Acceptance Criteria (BDD)**:  
`Given` a pending market update exists,  
`When` the user attempts deletion,  
`Then` the system prompts a confirmation  

---
### User Reactivates a Deleted Record

#### Test Case ID: USR-11
**Scenario**: User manually reactivates a previously deleted record  
**Preconditions**: A record exists in inactive status  
**Expected Result**: The system marks the record as active and logs the reactivation  
**Acceptance Criteria (BDD)**:  
`Given` a record is inactive,  
`When` the user reactivates it,  
`Then` the system marks it as active and logs the change  

---

#### Test Case ID: USR-12
**Scenario**: Market update arrives for a deactivated record  
**Preconditions**: The record exists but is inactive  
**Expected Result**: The system does not automatically reactivate the record—user intervention is required  
**Acceptance Criteria (BDD)**:  
`Given` a record is inactive,  
`When` a market update arrives,  
`Then` the system does not reactivate it without user approval  

---

#### Test Case ID: USR-13
**Scenario**: User requests full audit history of a deactivated record  
**Preconditions**: A record exists and has been modified manually or by the market  
**Expected Result**: The system provides a log of manual and market-driven changes, showing deactivation and reactivation timestamps  
**Acceptance Criteria (BDD)**:  
`Given` a record has history,  
`When` the user requests an audit log,  
`Then` the system provides a complete change history  

---
### Conflict Resolution Between Market and User-Generated Changes

#### Test Case ID: USR-15
**Scenario**: User accepts the market update despite a previous manual change  
**Preconditions**: A conflicting market update exists  
**Expected Result**: The system updates the record and removes the manual override flag  
**Acceptance Criteria (BDD)**:  
`Given` a conflicting market update exists,  
`When` the user accepts it,  
`Then` the system updates the record and resumes market-driven updates  

---

#### Test Case ID: USR-16
**Scenario**: User rejects the market update and keeps the manual version  
**Preconditions**: A conflicting market update exists  
**Expected Result**: The system blocks future automatic updates for the modified fields  
**Acceptance Criteria (BDD)**:  
`Given` a conflicting market update exists,  
`When` the user rejects it,  
`Then` the system prevents future updates to the affected fields  

---
### Logging & Audit Requirements

#### Test Case ID: USR-17
**Scenario**: User modifies a record  
**Preconditions**: The record exists  
**Expected Result**: The system logs who changed what and when  
**Acceptance Criteria (BDD)**:  
`Given` a record exists,  
`When` the user modifies it,  
`Then` the system logs the change with timestamps  
