--###################### Creation Queries ######################

-- Inserting with Property line 2
Insert into Property (propertyAddress, propertyAddressLine2, propertyState, propertyCity, propertyZip, numOfBedroom, numOfBathroom,keyNumber,pool,pets
bbq,airConditioning,washerDryer,numOfParkingSpots,outsideShower,wifiName,wifiPassword,beachside,bayside,oceanFront,bayFront,
commissionPercentage,OwnerID)
();

-- Create a pricing for a property
Insert INTO Pricing (startDate, endDate, propertyID, weeklyRate, dailyRate)
VALUES

--Insert into Tenant
INSERT INTO Tenant (LastName, FirstName, Email, phoneNumber, mailingAddress, mailingAddressLine2, mailingCity, mailingState, mailingZip)


-- Insert into leases
Insert into Leases (startDate, endDate, price, rentalInsurance, leaseStatus,rentalAgent,tenantID,propertyID) 
VALUES

--Insert into unavailability
INSERT INTO unavailability (startDate, endDate,reason,PropertyID,LeaseID)
VALUES


--###################### Search Queries ######################







--###################### REportQueries ######################