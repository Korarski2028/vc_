  #progress-container {
    2             display: none;
    3             margin-top: 20px;
    4         }
    5         .progress {
    6             height: 20px;
    7             background-color: #e0e0e0; /* Darker background for better visibility */
    8             border-radius: 10px;
    9             overflow: hidden;
   10         }
   11         .progress-bar {
   12             width: 100%; /* Explicitly set width */
   13             height: 100%;
   14             background: linear-gradient(to right, #016fd0 0%, #4caf50 50%, #016fd0 100%);
   15             background-size: 200% 100%;
   16             -webkit-animation: progress-animation 2s linear infinite; /* For Safari/Chrome */
   17             animation: progress-animation 2s linear infinite;
   18         }
   19         @-webkit-keyframes progress-animation {
   20             0% { background-position: 100% 0; }
   21             100% { background-position: -100% 0; }
   22         }
   23         @keyframes progress-animation {
   24             0% {
   25                 background-position: 100% 0;
   26             }
   27             100% {
   28                 background-position: -100% 0;
   29             }
   30         }