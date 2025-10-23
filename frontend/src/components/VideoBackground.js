import React from 'react';
import './VideoBackground.css';

const VideoBackground = ({ children }) => {
  return (
    <div className="video-background-container">
      <video 
        autoPlay 
        loop 
        muted 
        playsInline 
        className="video-background"
      >
        <source src="/assets/videos/background.mp4" type="video/mp4" />
      </video>
      <div className="video-overlay"></div>
      <div className="content-wrapper">
        {children}
      </div>
    </div>
  );
};

export default VideoBackground;
