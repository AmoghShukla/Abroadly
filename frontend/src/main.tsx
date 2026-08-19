import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import App from "./App";

const theme = createTheme({
  palette: { primary: { main: "#2156d8" }, secondary: { main: "#18a17f" }, background: { default: "#f6f8fc" } },
  typography: { fontFamily: "Inter, system-ui, sans-serif", h2: { fontWeight: 750 }, h5: { fontWeight: 700 } },
  shape: { borderRadius: 14 },
});

createRoot(document.getElementById("root")!).render(<StrictMode><ThemeProvider theme={theme}><CssBaseline /><App /></ThemeProvider></StrictMode>);
