import React, { useState, useEffect } from 'react';

// 1. Recursive Component for the Tree
const CommentNode = ({ comment, allComments }) => {
  // Find immediate children of this specific comment
  const children = allComments.filter(c => c.parent === comment.id);

  return (
    <div style={{ marginLeft: "20px", borderLeft: "2px solid #ddd", paddingLeft: "10px" }}>
      <div className="comment-header">
        <strong>{comment.author_name}</strong>
      </div>
      <p>{comment.content}</p>
      
      {/* Recursion: The component renders itself for children */}
      {children.map(child => (
        <CommentNode key={child.id} comment={child} allComments={allComments} />
      ))}
    </div>
  );
};

// 2. Main Post View
const PostView = ({ postId }) => {
  const [post, setPost] = useState(null);

  useEffect(() => {
    // Fetch data (Simulated URL)
    fetch(`/api/posts/${postId}/`)
      .then(res => res.json())
      .then(data => setPost(data));
  }, [postId]);

  if (!post) return <div>Loading...</div>;

  // Filter for top-level comments (parent is null)
  const rootComments = post.comments.filter(c => c.parent === null);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">{post.content}</h1>
      <p className="text-gray-500">By {post.author_name}</p>
      
      <div className="mt-6">
        <h3 className="font-bold">Comments</h3>
        {rootComments.map(comment => (
          // Pass the FULL list of comments down so children can find their own children
          <CommentNode key={comment.id} comment={comment} allComments={post.comments} />
        ))}
      </div>
    </div>
  );
};

export default PostView;