import React, { useState, useEffect } from "react";


const Navbar = (props) => {
    return (
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a
            class={"nav-link" + (props.page == "Home" ? " active" : "")}
            style={{ color: "#18BC9C" }}
            onClick={() => props.setPage("Home")}
          >
            Home
          </a>
        </li>
        <li class="nav-item">
          <a
            class={"nav-link" + (props.page == "Graph" ? " active" : "")}
            style={{ color: "#18BC9C" }}
            onClick={() => props.setPage("Graph")}
          >
            Graph
          </a>
        </li>
        <li class="nav-item">
          <a
            class={"nav-link" + (props.page == "Settings" ? " active" : "")}
            style={{ color: "#18BC9C" }}
            onClick={() => props.setPage("Settings")}
          >
            Settings
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/">
            Logout
          </a>
        </li>
      </ul>
    );
  };
  
  export default Navbar;