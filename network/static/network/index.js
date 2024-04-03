document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-form').forEach((form) => {
        form.style.display = 'none' 
    })

    fetch(`/my_posts`)
    .then(response => response.json())
    .then(post => {
        my_posts_id = post.map(({id})=>id)
        document.querySelectorAll('.edit-button').forEach((button) => {
            if ((my_posts_id.includes(Number(button.parentNode.id)))) {
                button.style.display = 'block'
            }
        })
    })

    fetch(`/like_posts`)
    .then(response => response.json())
    .then(post => {
        like_posts_id = post.map(({id})=>id)
        document.querySelectorAll('.post').forEach((post) => {
            if ((like_posts_id.includes(Number(post.id)))) {
                post.querySelector('#like-button').style.display = 'none'
            }
            else {
                post.querySelector('#unlike-button').style.display = 'none'
            }
        })
    })

    document.querySelectorAll('.edit-button').forEach((button) => {
        const post = button.parentNode

        button.onclick = () => {        
            post.querySelector('.edit-form').style.display = 'block'
            post.querySelector('.content').style.display = 'none'
        }
    })

    

    document.querySelectorAll('#submit-button').forEach((button) => {
        button.onclick = () => {
            post = button.parentNode.parentNode
            fetch(`/posts/${post.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: post.querySelector('textarea').value
                })
            })
            post.querySelector('.content').innerHTML = post.querySelector('textarea').value
            post.querySelector('.edit-form').style.display = 'none'
            post.querySelector('.content').style.display = 'block'            
        }
    })

    document.querySelectorAll('#like-button').forEach((button) => {
        button.onclick = () => {
            post = button.parentNode
            fetch(`/posts/${post.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    add_like_user: true
                })
            })
            post.querySelector('#like-button').style.display = 'none'
            post.querySelector('#unlike-button').style.display = 'inline'
            post.querySelector('#sum-like').innerHTML++
        }
    })

    document.querySelectorAll('#unlike-button').forEach((button) => {
        button.onclick = () => {
            post = button.parentNode
            fetch(`/posts/${post.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    remove_like_user: true
                })
            })
            post.querySelector('#like-button').style.display = 'inline'
            post.querySelector('#unlike-button').style.display = 'none'
            post.querySelector('#sum-like').innerHTML--
        }
    })
})