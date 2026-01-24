document.getElementById("searchButton").addEventListener("click", function () {
    const searchContainer = document.getElementById("searchContainer");
    searchContainer.classList.toggle("active"); // Toggle active class
  });

  // Handle search form submission
  document.getElementById("searchForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    let searchQuery = document.getElementById("searchInput").value;
    let response = await fetch('/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ search: searchQuery })
    });

    let result = await response.json();
    if (result.redirect) {
      window.location.href = result.redirect;
    } else {
      alert(result.message);
    }
  });
document.addEventListener('DOMContentLoaded', function() {
// Page starts at top
window.scrollTo(0, 0);

// Nutrition items animation
const nutritionItems = document.querySelectorAll('.nutrition-item');
nutritionItems.forEach((item, index) => {
  setTimeout(() => {
    item.classList.add('show');
  }, index * 200);
});

// Initialize AOS animations for all sections
AOS.init({
  duration: 800,
  easing: 'ease-in-out',
  once: false
});
});
function toggleComments() {
  let commentsDiv = document.getElementById('comments');
  if (commentsDiv.style.display === "none" || commentsDiv.style.display === "") {
      commentsDiv.style.display = "block";
      
      // Only fetch if there are no server-rendered comments
      if (commentsDiv.querySelector('.comment') === null) {
          fetchComments();
      }
  } else {
      commentsDiv.style.display = "none";
  }
}

function fetchComments() {
  let recipeName = document.getElementById('title').textContent.trim();
  if (!recipeName) {
      console.error("Recipe name is missing.");
      return;
  }
  let fetchUrl = `/get_comments/${encodeURIComponent(recipeName)}`;
  console.log("Fetching comments from:", fetchUrl);

  fetch(fetchUrl)
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
  })
  .then(data => {
      console.log("Received comments:", data);
      let commentsDiv = document.getElementById('comments');
      
      if (data.length > 0) {
          commentsDiv.innerHTML = data.map(comment => `
              <div class="comment" style="margin-bottom: 10px; display: flex; justify-content: space-between; align-items: baseline;">
                  <div style="flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                      <span style="color: #c50202; font-weight: bold;">${comment.user}: </span>
                      <span style="color: #333;">${comment.comment}</span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 10px;">
                      <span style="color: #888; font-size: 0.8em; white-space: nowrap;">${comment.timestamp}</span>
                      ${comment.canDelete ? 
                          `<button onclick="deleteComment(${comment.id})" 
                              style="background: #ff4d4d; 
                                     color: white; 
                                     border: none; 
                                     padding: 2px 8px; 
                                     border-radius: 12px; 
                                     font-size: 0.7em; 
                                     cursor: pointer;
                                     transition: all 0.3s ease;"
                              onmouseover="this.style.background='#cc0000'"
                              onmouseout="this.style.background='#ff4d4d'">
                              Delete
                          </button>` : ''}
                  </div>
              </div>
          `).join('');
      } else {
          commentsDiv.innerHTML = "<p style='color: #666; text-align: center;'>No comments yet. Be the first to comment!</p>";
      }
  })
  .catch(error => console.error("Error fetching comments:", error));
}

function deleteComment(commentId) {
    if (!confirm('Are you sure you want to delete this comment?')) {
        return;
    }
    
    fetch(`/delete_comment/${commentId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Failed to delete comment'); });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Refresh comments after deletion
            fetchComments();
        } else {
            alert('Failed to delete comment: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    });
}

function showCommentForm() {
document.getElementById('comments-initial-view').classList.add('animate__fadeOut');
setTimeout(() => {
document.getElementById('comments-initial-view').style.display = 'none';
document.getElementById('comments-form-view').style.display = 'block';
document.getElementById('comments-form-view').classList.add('animate__fadeIn');
document.querySelector('.comment-textarea').focus();
}, 300);
}

function showCommentsView() {
document.getElementById('comments-form-view').classList.add('animate__fadeOut');
setTimeout(() => {
document.getElementById('comments-form-view').style.display = 'none';
document.getElementById('comments-initial-view').style.display = 'block';
document.getElementById('comments-initial-view').classList.add('animate__fadeIn');
// Smooth scroll to comments
document.getElementById('comments-display').scrollIntoView({ behavior: 'smooth' });
}, 300);
}

// Initialize with animation
document.addEventListener('DOMContentLoaded', function() {
document.getElementById('comments-initial-view').classList.add('animate__fadeIn');
});