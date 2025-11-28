/* Sidebar Account Context Menu Setup */
let selectedAccount = null;
let selectedAccountId = null;
let selectedAccountName = null;

document.querySelectorAll('.account-item').forEach(item => {
  item.addEventListener('contextmenu', (e) => {
    e.preventDefault();

    if (selectedAccount) {
      selectedAccount.classList.remove('selected');
      selectedAccount = null;
    }
    item.classList.add('selected');
    selectedAccount = item;

    selectedAccountId = item.dataset.accountId;
    selectedAccountName = item.dataset.accountName;

    const menu = document.getElementById('account-context-menu');
    menu.style.display = 'block';
    menu.style.left = e.pageX + 'px';
    menu.style.top = e.pageY + 'px';
  });
});

document.addEventListener('click', () => {
  document.getElementById('account-context-menu').style.display = 'none';

  if (selectedAccount) {
    selectedAccount.classList.remove('selected');
    selectedAccount = null;
  }
});

document.getElementById('delete-account').addEventListener('click', () => {
  if (confirm(`Delete Account "${selectedAccountName}"?`)) {
    fetch(`/accounts/${selectedAccountId}`, {
      method: 'DELETE'
    }).then(response => {
        if (response.ok) {
          const accountElement = document.querySelector(`[data-account-id="${selectedAccountId}"`);
          accountElement.remove();
        } else {
          alert('Failed to delete account.');
        }
      });
  }
});

/* Transaction Log Context Menu Setup */
let selectedRow = null;
let selectedTransactionId = null;
let selectedTransaction = null;

document.querySelectorAll('.transaction-row').forEach(row => {
  row.addEventListener('contextmenu', (e) => {
    e.preventDefault();

    if (selectedRow) {
      selectedRow.classList.remove('selected');
      selectedRow = null;
      selectedTransaction = null;
    }

    row.classList.add('selected');
    selectedRow = row;

    selectedTransactionId = row.dataset.transactionId;

    selectedTransaction = {
      id: row.dataset.transactionId,
      description: row.dataset.description,
      date: row.dataset.date,
      amount: row.dataset.amount,
      debitAccountId: row.dataset.debitAccountId,
      creditAccountId: row.dataset.creditAccountId
    };

    const menu = document.getElementById('transaction-context-menu');
    menu.style.display = 'block';
    menu.style.left = e.pageX + 'px';
    menu.style.top = e.pageY + 'px';
  });
});

document.addEventListener('click', () => {
  document.getElementById('transaction-context-menu').style.display = 'none';

  if (selectedRow) {
    selectedRow.classList.remove('selected');
    selectedRow = null;
    selectedTransaction = null;
  }
});

document.getElementById('delete-transaction').addEventListener('click', () => {
  if (confirm(`Delete Transaction "${selectedTransactionId}"?`)) {
    fetch(`/transactions/${selectedTransactionId}`, {
      method: 'DELETE'
    }).then(response => {
        if (response.ok) {
          window.location.reload();
        } else {
          alert('Failed to delete transaction.');
        }
      });
  }
});

/* Account Transaction Filtering */
document.querySelectorAll('.account-item').forEach(item => {
  item.addEventListener('click', () => {
    const accountId = item.dataset.accountId;
    const accountName = item.dataset.accountName;

    const mainTitleElement = document.getElementById('main-title');
    mainTitleElement.textContent = accountName;

    const clearFilterBtn = document.getElementById('clear-filter-btn');
    clearFilterBtn.style.display = '';

    filterTransactions(accountId);

    document.querySelectorAll('.account-item').forEach(i => i.classList.remove('selected'));
    item.classList.add('selected');
  });
});

function filterTransactions(accountId) {
  const transactionRows = document.querySelectorAll('.transaction-row');

  if (!accountId) {
    transactionRows.forEach(row => row.style.display = '');
    return;
  }

  transactionRows.forEach(row => {
    const debitAccountId = row.dataset.debitAccountId;
    const creditAccountId = row.dataset.creditAccountId;

    if (accountId === debitAccountId || accountId === creditAccountId) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

document.getElementById('clear-filter-btn').addEventListener('click', () => {
  const mainTitleElement = document.getElementById('main-title');
  mainTitleElement.textContent = 'Transactions';

  const clearFilterBtn = document.getElementById('clear-filter-btn');
  clearFilterBtn.style.display = 'none';

  filterTransactions(null);

  document.querySelectorAll('.account-item').forEach(i => i.classList.remove('selected'));
});

/* Account Modal */
const accountModal = document.getElementById('account-modal');
const addAccountBtn = document.getElementById('add-account-btn');
const closeAccountModalBtn = document.querySelector('[data-modal="account-modal"]');

addAccountBtn.addEventListener('click', (e) => {
  e.preventDefault();
  accountModal.style.display = 'flex';
  document.getElementById('account-name').focus();
});

closeAccountModalBtn.addEventListener('click', (e) => {
  e.preventDefault();
  accountModal.style.display = 'none';
});
accountModal.addEventListener('click', (e) => {
  if (e.target === accountModal) {
    accountModal.style.display = 'none';
  }
});

function updateNormalBalance() {
  const accountType = document.getElementById('account-type').value;
  const normalBalanceField = document.getElementById('account-normal-balance');

  const normalBalances = {
    'ASSET': 'Debit',
    'LIABILITY': 'Credit',
    'EQUITY': 'Credit',
    'EXPENSE': 'Debit',
    'INCOME': 'Credit'
  };

  if (accountType && normalBalances[accountType]) {
    normalBalanceField.value = normalBalances[accountType];
  } else {
    normalBalanceField.value = '';
  }
}

// Add Account Modal Validation
document.getElementById('account-form').addEventListener('submit', function(e) {
  const accountName = document.getElementById('account-name').value.trim();
  const accountType = document.getElementById('account-type').value;

  if (!accountName) {
    alert('Please enter an account name.');
    e.preventDefault();
    return;
  }

  if (!accountType) {
    alert('Please select an account type.');
    e.preventDefault();
    return;
  }
});

/* Edit Account Modal */
const editAccountModal = document.getElementById('edit-account-modal');
const editAccountForm = document.getElementById('edit-account-form');
const closeEditAccountModalBtn = document.querySelector('[data-modal="edit-account-modal"]');

document.getElementById('rename-account').addEventListener('click', () => {
  document.getElementById('edit-account-id').value = selectedAccountId;
  document.getElementById('edit-account-name').value = selectedAccountName;

  editAccountForm.action = `/accounts/${selectedAccountId}`;

  editAccountModal.style.display = 'flex';
  document.getElementById('edit-account-name').focus();
});

closeEditAccountModalBtn.addEventListener('click', () => {
  editAccountModal.style.display = 'none';
});

editAccountModal.addEventListener('click', (e) => {
  if (e.target === editAccountModal) {
    editAccountModal.style.display = 'none';
  }
});

/* Add Transaction Modal */
const transactionModal = document.getElementById('transaction-modal');
const addTransactionBtn = document.getElementById('add-transaction-btn');
const closeTransactionModalBtn = document.querySelector('[data-modal="transaction-modal"]');

addTransactionBtn.addEventListener('click', (e) => {
  e.preventDefault();
  transactionModal.style.display = 'flex';
  document.getElementById('transaction-description').focus();
});
closeTransactionModalBtn.addEventListener('click', (e) => {
  e.preventDefault();
  transactionModal.style.display = 'none';
});
transactionModal.addEventListener('click', (e) => {
  if (e.target === transactionModal) {
    transactionModal.style.display = 'none';
  }
});

/* Edit Transaction Modal */
const editTransactionModal = document.getElementById('edit-transaction-modal');
const editTransactionForm = document.getElementById('edit-transaction-form');
const closeEditTransactionModalBtn = document.querySelector('[data-modal="edit-transaction-modal"]');

document.getElementById('edit-transaction').addEventListener('click', () => {
  document.getElementById('edit-transaction-id').value = selectedTransaction.id;
  document.getElementById('edit-transaction-description').value = selectedTransaction.description;
  document.getElementById('edit-transaction-date').value = selectedTransaction.date;
  document.getElementById('edit-transaction-amount').value = selectedTransaction.amount;
  document.getElementById('edit-transaction-debit-account-id').value = selectedTransaction.debitAccountId;
  document.getElementById('edit-transaction-credit-account-id').value = selectedTransaction.creditAccountId;

  editTransactionForm.action = `/transactions/${selectedTransactionId}`;
  editTransactionModal.style.display = 'flex';
  document.getElementById('edit-transaction-description').focus();
});

closeEditTransactionModalBtn.addEventListener('click', () => {
  editTransactionModal.style.display = 'none';
});

editTransactionModal.addEventListener('click', (e) => {
  if (e.target === editTransactionModal) {
    editTransactionModal.style.display = 'none';
  }
});

// Close modals when ESC is pressed
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' || e.key === 'Esc') {
    const isAccountModalOpen = document.getElementById('account-modal').style.display === 'flex';
    const isEditAccountModalOpen = document.getElementById('edit-account-modal').style.display === 'flex';
    const isTransactionModalOpen = document.getElementById('transaction-modal').style.display === 'flex';
    const isEditTransactionModalOpen = document.getElementById('edit-transaction-modal').style.display === 'flex';
    if (isAccountModalOpen || isEditAccountModalOpen || isTransactionModalOpen || isEditTransactionModalOpen) {
      document.getElementById('account-modal').style.display = 'none';
      document.getElementById('edit-account-modal').style.display = 'none';
      document.getElementById('transaction-modal').style.display = 'none';
      document.getElementById('edit-transaction-modal').style.display = 'none';
    } else {
      const clearFilterBtn = document.getElementById('clear-filter-btn');
      if (clearFilterBtn.style.display !== 'none') {
        clearFilterBtn.click();
      }
    }
  }
});

