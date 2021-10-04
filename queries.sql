-- Inserting without Property line 2
Insert into Property (propertyAddress, propertyState, propertyCity, propertyZip, numOfBedroom, numOfBathroom,keyNumber,pool,pets
bbq,airConditioning,washerDryer,numOfParkingSpots,outsideShower,wifiName,wifiPassword,beachside,bayside,oceanFront,bayFront,
commissionPercentage,OwnerID)
();

-- Inserting with Property line 2
Insert into Property (propertyAddress, propertyAddressLine2, propertyState, propertyCity, propertyZip, numOfBedroom, numOfBathroom,keyNumber,pool,pets
bbq,airConditioning,washerDryer,numOfParkingSpots,outsideShower,wifiName,wifiPassword,beachside,bayside,oceanFront,bayFront,
commissionPercentage,OwnerID)
();

-- Create a pricing for a property
Insert INTO Pricing (startDate, endDate, propertyID, weeklyRate, dailyRate)
VALUES
