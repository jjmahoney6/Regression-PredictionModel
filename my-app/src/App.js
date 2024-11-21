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
  const dayOptions = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  const handlePredict = async () => {
    try {
      const response = await axios.post('http://localhost:5000/predict', {
        weather,
        event,
        dayOfWeek,
      });
      setPredictedAttendance(response.data.predictedAttendance);
    } catch (error) {
      console.error("Error fetching prediction:", error);
    }
  };

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
            <Button variant="contained" color="primary" fullWidth onClick={handlePredict}>
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
