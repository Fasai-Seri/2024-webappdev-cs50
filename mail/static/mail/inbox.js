document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
  document.querySelector('#compose-form').onsubmit = () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    // console.log(recipients, subject, body)
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#selected-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      emails.forEach(email => {
        const email_div = document.createElement('div');

        if (mailbox === 'inbox') {
          email_div.innerHTML = 
          `
          <button class='archive-button' id=${email.id}>Archive</button>
          <div id=${email.id} class='email-div'>
            <span id='sender'>${email.sender}</span>
            <span id='subject'>${email.subject}</span>
            <span id='timestamp'>${email.timestamp}</span>
          </div>
          `
        }
        
        else if (mailbox === 'archive') {
          email_div.innerHTML = 
          `
          <button class='unarchive-button' id=${email.id}>Unarchive</button>
          <div id=${email.id} class='email-div'>
            <span id='sender'>${email.sender}</span>
            <span id='subject'>${email.subject}</span>
            <span id='timestamp'>${email.timestamp}</span>
          </div>
          `
        }

        else {
          email_div.innerHTML = 
          `
          <div id=${email.id} class='email-div'>
            <span id='sender'>${email.sender}</span>
            <span id='subject'>${email.subject}</span>
            <span id='timestamp'>${email.timestamp}</span>
          </div>
          `
        }
        if (email.read) {
          email_div.querySelector('div').classList.add('read')
        }

        email_div.querySelector('div').addEventListener('click', function() {
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#selected-email-view').style.display = 'block';

          fetch(`/emails/${this.id}`)
          .then(response => response.json())
          .then(email => {
              console.log(email.body);
              
              document.querySelector('#selected-email-view').innerHTML = 
              `
              <div id='header'>
                <p><b>From: </b>${email.sender}</p>
                <p><b>To: </b>${email.recipients}</p>
                <p><b>Subject: </b>${email.subject}</p>
                <p><b>Timestamp: </b>${email.timestamp}</p>
                <button>Reply</button>
              </div>
              <hr>
              <div id='body'>
                <p>${email.body}</p>
              </div>
              `
          });

          fetch(`/emails/${this.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })

        });

        document.querySelector('#emails-view').append(email_div);

        document.querySelectorAll('.archive-button').forEach((button) => {
          button.onclick = () => {
            // console.log('archive')
            
            fetch(`/emails/${button.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: true
              })   
            })
            load_mailbox('inbox')
          }
        })

        document.querySelectorAll('.unarchive-button').forEach((button) => {
          button.onclick = () => {

            fetch(`/emails/${button.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: false
              })
            })
            // load_mailbox('inbox');
          }
        })
      })
  });
}