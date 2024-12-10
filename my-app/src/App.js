import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { Button, TextField, MenuItem, Typography, Container, Paper, Grid } from '@mui/material';

function App() {
  const [weather, setWeather] = useState('');
  const [event, setEvent] = useState('');
  const [dayOfWeek, setDayOfWeek] = useState('');
  const [predictedAttendance, setPredictedAttendance] = useState(null);

  const weatherOptions = ['Sunny', 'Clear', 'Partly Cloudy', 'Cloudy', 'Overcast', 'Drizzle', 'Rain'];
  const eventOptions = ['Opening Day', 'Fireworks', 'Promotions', 'Regular', 'None'];
  const dayOptions = ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  const [loading, setLoading] = useState(false);
  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/predict', {
        weather: weather, // Send weather string directly
        event: event,     // Send event string directly
        temp_weight: 0,   // Optional defaults
        prev_sales_1: 0,
        prev_sales_2: 0,
        rolling_mean_3: 0,
        day_of_week: dayOfWeek.charAt(0).toUpperCase() + dayOfWeek.slice(1), // Capitalize the first letter
      });
      setPredictedAttendance(response.data.predicted_attendance);
    } catch (error) {
      console.error("Error fetching prediction:", error);
    } finally {
      setLoading(false);
    }
  };  
  const isFormValid = weather && event && dayOfWeek;

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} style={{ padding: '20px', marginTop: '30px' }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Attendance Prediction
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              select
              fullWidth
              label="Weather"
              value={weather}
              onChange={(e) => setWeather(e.target.value)}
              variant="outlined"
            >
              {weatherOptions.map((option) => (
                <MenuItem key={option} value={option.toLowerCase()}>
                  {option}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField
              select
              fullWidth
              label="Event"
              value={event}
              onChange={(e) => setEvent(e.target.value)}
              variant="outlined"
            >
              {eventOptions.map((option) => (
                <MenuItem key={option} value={option.toLowerCase()}>
                  {option}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField
              select
              fullWidth
              label="Day of the Week"
              value={dayOfWeek}
              onChange={(e) => setDayOfWeek(e.target.value)}
              variant="outlined"
            >
              {dayOptions.map((option) => (
                <MenuItem key={option} value={option.toLowerCase()}>
                  {option}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" color="primary" fullWidth onClick={handlePredict} disabled={!isFormValid}>
              Predict Attendance
            </Button>
          </Grid>
        </Grid>
        {predictedAttendance !== null && (
          <Typography variant="h5" align="center" style={{ marginTop: '20px' }}>
            Predicted Attendance: {predictedAttendance}
          </Typography>
        )}
      </Paper>
    </Container>
  );
}

export default App; // Export App instead of Body
