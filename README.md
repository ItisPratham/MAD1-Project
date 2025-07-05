# vehicle-parking-app
This is the github repo for my MAD1 Project of May2025 Term.

Vehicle Parking App - V1
It is a multi-user app (one requires an administrator and other users) that manages different parking lots, parking spots and parked vehicles. Assume that this parking app is for 4-wheeler parking.

23rd June 2025
Milestone1 Completed
Created models for user, admin(predefined user), parking lot, parking spot and reserve parking spot.
This database tables are created programmatically using python not manually.
Also established relationships wherever required.
ie
A user can have multiple reserve parking spot history.
A parking lot will have multiple parking spots.
A parking spots will have multiple reserve parking spots history.

29th June 2025
Milestone2 Completed
Implemented User registration and login with required fields.
Created an Admin login in which admin is predifined so no registration.
Redirect to role-specific dashboards after login, although dashboards are not yet created.
Added sessions so to prevent unauthorized access to routes.
ie
Without login, user as well as admin cannot access their dashboards.

3rd July 2025
Milestone3 Completed
Added Admin functionalities
Create/edit/delete parking lots.
View parking lot details and spot status in dashboard.
Automatically create parking spots based on the maximum capacity of the lot.
View parking spots details ie current and past reservations.
Admin will be able to see all the user's and also individual users' track record.

5th July 2025
Milestone4 Completed
Added following to User functionalities:
View available parking lots.
Auto-allocation/Reservation of the first available spot.
Occupy and Release a spot while tracking timestamp.
Track timestamps for reservation and View parking history.
Show duration of parking spot once its released.
Auto calculation of total cost once the spot is released.
View current active parkings.
Edit User details.