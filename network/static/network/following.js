document.addEventListener('DOMContentLoaded', () => {
    
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