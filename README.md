# vehicle-parking-app

This is the github repo for my MAD1 Project of May2025 Term.

## Vehicle Parking App - V1

It is a multi-user app (one requires an administrator and other users) that manages different parking lots, parking spots and parked vehicles. Assume that this parking app is for 4-wheeler parking.

---

### 23rd June 2025  
**Milestone1 Completed : Database Models and Schema Setup**  
Created models for user, admin(predefined user), parking lot, parking spot and reserve parking spot.  
This database tables are created programmatically using python not manually.  
Also established relationships wherever required.  
ie  
A user can have multiple reserve parking spot history.  
A parking lot will have multiple parking spots.  
A parking spots will have multiple reserve parking spots history.

---

### 29th June 2025  
**Milestone2 Completed : Authentication and Role-Based Access**  
Implemented User registration and login with required fields.  
Created an Admin login in which admin is predifined so no registration.  
Redirect to role-specific dashboards after login, although dashboards are not yet created.  
Added sessions so to prevent unauthorized access to routes.  
ie  
Without login, user as well as admin cannot access their dashboards.

---

### 3rd July 2025  
**Milestone3 Completed : Admin Dashboard and Lot/Spot Management**  
Added Admin functionalities  
Create/edit/delete parking lots.  
View parking lot details and spot status in dashboard.  
Automatically create parking spots based on the maximum capacity of the lot.  
View parking spots details ie current and past reservations.  
Admin will be able to see all the user's and also individual users' track record.

---

### 5th July 2025  
**Milestone4 Completed : User Dashboard and Reservation/Parking System**  
Added following to User functionalities:  
View available parking lots.  
Auto-allocation/Reservation of the first available spot.  
Occupy and Release a spot while tracking timestamp.  
Track timestamps for reservation and View parking history.  
Show duration of parking spot once its released.  
Auto calculation of total cost once the spot is released.  
View current active parkings.  
Edit User details.

---

### 6th July 2025  
**Milestone 5 & 6 Completed : Reservation/Parking History and Summary, Slot Time Calculation and Parking Cost**  
Realised few of the objectives of milestone 5&6 were previously completed in previous milestones unknowingly.  
Added following functionalites:  
Added User's ddedicated parking history tab that will contain all past records.  
Added Chart's to user, that will display various statics wrt Parking Lots.  
Used base_user_dashboard.html to simplify user tabs.  
Added dedicated parking record's tab for admin to view.  
Added admin summary which displays a pie chart and a stacked bar chart along with a table, all of whom has properties related to parking lots.  
Modified:  
Logout button to side with edit profile for consistency in both admin and user interface.  
Also added if else when displaying various records, so if no records are found then will not display table heads.  
Note: Charts were created using Chart.js, which i learned basics of with the help of documentation as well as youtube videos.(Learned for first time.)

---

### CORE FUNCTIONALITIES ARE COMPLETED WITH MAYBE FEW PARTIAL RECOMMENDED/OPTIONAL ENHANCEMENTS

---

### 9th July 2025
**Milestone: Flask Login Integration and Security, Milestone: Charts and Visualization**  
Integrate Flask-Login and Restrict routes and protect sessions.  
This was done by using flask-login package.  
Logins were managed by LoginManager, it redirects to userlogin by default if not logged in with decorator(login_manager which implemets a method of usermixin).  
And added password storage hashing using werkzeug.security, by adding methods to the user db logic(set and check password implementing generate and check password hash respectively).  
Charts and Visualizations were previously unknowingly completed while completing milestone5&6.  

---