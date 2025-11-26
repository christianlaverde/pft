-- Insert accounts
INSERT INTO accounts (name, type, is_active) VALUES
('Checking', 'ASSET', 1),
('Savings', 'ASSET', 1),
('Cash', 'ASSET', 1),
('Credit Card', 'LIABILITY', 1),
('Equity', 'EQUITY', 1),
('Salary', 'INCOME', 1),
('Freelance', 'INCOME', 1),
('Groceries', 'EXPENSE', 1),
('Rent', 'EXPENSE', 1),
('Utilities', 'EXPENSE', 1),
('Gas', 'EXPENSE', 1),
('Restaurants', 'EXPENSE', 1),
('Coffee', 'EXPENSE', 1),
('Entertainment', 'EXPENSE', 1),
('Shopping', 'EXPENSE', 1),
('Healthcare', 'EXPENSE', 1),
('Internet', 'EXPENSE', 1),
('Phone', 'EXPENSE', 1);

-- Opening balances (Nov 1)
INSERT INTO transactions (description, date, amount, debit_account_id, credit_account_id, is_active) VALUES
('Opening Balance for Checking', '2025-09-14', 2850.00, 1, 5, 1),
('Opening Balance for Savings', '2025-09-14', 5000.00, 2, 5, 1),
('Opening Balance for Cash', '2025-09-14', 120.00, 3, 5, 1),
-- Sept 15 - PAYDAY!
('Biweekly Salary Payment', '2025-09-15', 3725.25, 1, 6, 1),
-- Sept 15 - Transfer to savings
('Transfer to Savings', '2025-09-15', 500.00, 2, 1, 1),
-- Sept 16 - Groceries
('Grocery Shopping - HEB', '2025-09-16', 102.45, 8, 1, 1),
-- Sept 17 - Gas and coffee
('Gas Station Fill-up', '2025-09-17', 44.30, 11, 1, 1),
('Coffee Shop', '2025-09-17', 5.25, 13, 1, 1),
-- Sept 19 - Restaurants
('Lunch - Local Deli', '2025-09-19', 15.80, 12, 1, 1),
-- Sept 20 - Entertainment
('Concert Tickets', '2025-09-20', 75.00, 14, 4, 1),
-- Sept 21 - Groceries
('Grocery Shopping - HEB', '2025-09-21', 88.92, 8, 1, 1),
-- Sept 22 - Coffee
('Coffee Shop', '2025-09-22', 6.50, 13, 1, 1),
-- Sept 24 - Gas
('Gas Station Fill-up', '2025-09-24', 46.15, 11, 1, 1),
-- Sept 25 - Shopping
('Home Depot Purchase', '2025-09-25', 134.56, 15, 4, 1),
-- Sept 26 - Restaurants
('Dinner Out', '2025-09-26', 62.40, 12, 4, 1),
-- Sept 28 - Groceries
('Grocery Shopping - HEB', '2025-09-28', 95.67, 8, 1, 1),
-- Sept 29 - PAYDAY!
('Biweekly Salary Payment', '2025-09-29', 3725.25, 1, 6, 1),
-- Sept 29 - Transfer to savings
('Transfer to Savings', '2025-09-29', 500.00, 2, 1, 1),
-- Sept 30 - Coffee
('Coffee Shop', '2025-09-30', 5.75, 13, 1, 1),
-- Oct 1 - Rent paid
('Monthly Rent Payment', '2025-10-01', 1200.00, 9, 1, 1),
-- Oct 2 - Groceries
('Grocery Shopping - HEB', '2025-10-02', 91.23, 8, 1, 1),
-- Oct 3 - Gas and utilities
('Gas Station Fill-up', '2025-10-03', 47.80, 11, 1, 1),
('Electric Bill', '2025-10-03', 98.75, 10, 1, 1),
-- Oct 5 - Internet and phone bills
('Internet Bill - Spectrum', '2025-10-05', 79.99, 17, 1, 1),
('Phone Bill - T-Mobile', '2025-10-05', 65.00, 18, 1, 1),
-- Oct 7 - Groceries
('Grocery Shopping - HEB', '2025-10-07', 118.45, 8, 1, 1),
-- Oct 8 - Coffee
('Coffee Shop', '2025-10-08', 6.00, 13, 1, 1),
-- Oct 10 - Gas
('Gas Station Fill-up', '2025-10-10', 45.90, 11, 1, 1),
-- Oct 11 - Restaurants
('Lunch - Food Truck', '2025-10-11', 12.50, 12, 1, 1),
-- Oct 13 - PAYDAY!
('Biweekly Salary Payment', '2025-10-13', 3725.25, 1, 6, 1),
-- Oct 13 - Transfer to savings
('Transfer to Savings', '2025-10-13', 500.00, 2, 1, 1),
-- Oct 14 - Shopping
('Target Run', '2025-10-14', 67.34, 15, 4, 1),
-- Oct 16 - Groceries
('Grocery Shopping - HEB', '2025-10-16', 103.78, 8, 1, 1),
-- Oct 17 - Gas and coffee
('Gas Station Fill-up', '2025-10-17', 48.25, 11, 1, 1),
('Coffee Shop', '2025-10-17', 5.50, 13, 1, 1),
-- Oct 19 - Entertainment
('Movie Night', '2025-10-19', 28.00, 14, 1, 1),
-- Oct 20 - Restaurants
('Dinner Out', '2025-10-20', 58.90, 12, 4, 1),
-- Oct 21 - Groceries
('Grocery Shopping - HEB', '2025-10-21', 86.54, 8, 1, 1),
-- Oct 22 - Healthcare
('Prescription Refill', '2025-10-22', 25.00, 16, 1, 1),
-- Oct 24 - Gas
('Gas Station Fill-up', '2025-10-24', 46.70, 11, 1, 1),
-- Oct 25 - Coffee
('Coffee Shop', '2025-10-25', 6.25, 13, 1, 1),
-- Oct 27 - PAYDAY!
('Biweekly Salary Payment', '2025-10-27', 3725.25, 1, 6, 1),
-- Oct 27 - Transfer to savings
('Transfer to Savings', '2025-10-27', 500.00, 2, 1, 1),
-- Oct 27 - Pay off credit card
('Credit Card Payment', '2025-10-27', 350.00, 4, 1, 1),
-- Oct 28 - Groceries
('Grocery Shopping - HEB', '2025-10-28', 112.89, 8, 1, 1),
-- Oct 30 - Shopping
('Amazon Purchase', '2025-10-30', 42.99, 15, 4, 1),
-- Oct 31 - Halloween treats
('Halloween Candy', '2025-10-31', 35.67, 8, 1, 1),
-- Nov 1 - Rent paid
('Monthly Rent Payment', '2025-11-01', 1200.00, 9, 1, 1),
-- Nov 2 - Groceries
('Grocery Shopping - HEB', '2025-11-02', 87.43, 8, 1, 1),
('Coffee Shop', '2025-11-02', 5.75, 13, 1, 1),
-- Nov 3 - Gas and utilities
('Gas Station Fill-up', '2025-11-03', 45.20, 11, 1, 1),
('Electric Bill', '2025-11-03', 112.50, 10, 1, 1),
-- Nov 5 - Internet and phone bills
('Internet Bill - Spectrum', '2025-11-05', 79.99, 17, 1, 1),
('Phone Bill - T-Mobile', '2025-11-05', 65.00, 18, 1, 1),
-- Nov 7 - Groceries
('Grocery Shopping - HEB', '2025-11-07', 124.67, 8, 1, 1),
-- Nov 8 - Entertainment
('Movie Tickets', '2025-11-08', 32.00, 14, 4, 1),
('Dinner Out', '2025-11-08', 67.89, 12, 4, 1),
-- Nov 10 - Gas
('Gas Station Fill-up', '2025-11-10', 48.15, 11, 1, 1),
-- Nov 12 - Coffee and lunch
('Coffee Shop', '2025-11-12', 6.25, 13, 1, 1),
('Lunch - Chipotle', '2025-11-12', 13.45, 12, 1, 1),
-- Nov 14 - Shopping
('Amazon Purchase', '2025-11-14', 89.99, 15, 4, 1),
-- Nov 15 - PAYDAY!
('Biweekly Salary Payment', '2025-11-15', 3725.25, 1, 6, 1),
-- Nov 15 - Transfer to savings
('Transfer to Savings', '2025-11-15', 500.00, 2, 1, 1),
-- Nov 16 - Groceries
('Grocery Shopping - HEB', '2025-11-16', 95.34, 8, 1, 1),
-- Nov 17 - Gas and coffee
('Gas Station Fill-up', '2025-11-17', 46.80, 11, 1, 1),
('Coffee Shop', '2025-11-17', 5.50, 13, 1, 1),
-- Nov 19 - Doctor visit
('Doctor Copay', '2025-11-19', 35.00, 16, 1, 1),
-- Nov 20 - Restaurants
('Dinner Out', '2025-11-20', 54.32, 12, 4, 1),
-- Nov 21 - Groceries
('Grocery Shopping - HEB', '2025-11-21', 108.76, 8, 1, 1),
-- Nov 22 - Coffee
('Coffee Shop', '2025-11-22', 6.00, 13, 1, 1),
-- Nov 24 - Gas
('Gas Station Fill-up', '2025-11-24', 47.25, 11, 1, 1),
-- Nov 26 - Freelance income
('Freelance Project Payment', '2025-11-26', 850.00, 1, 7, 1),
-- Nov 27 - Pay off credit card
('Credit Card Payment', '2025-11-27', 300.00, 4, 1, 1),
-- Nov 28 - Groceries
('Grocery Shopping - HEB', '2025-11-28', 76.89, 8, 1, 1),
-- Nov 29 - PAYDAY!
('Biweekly Salary Payment', '2025-11-29', 3725.25, 1, 6, 1),
-- Nov 29 - Transfer to savings
('Transfer to Savings', '2025-11-29', 500.00, 2, 1, 1),
-- Nov 30 - End of month shopping
('Target Run', '2025-11-30', 45.67, 15, 1, 1);
