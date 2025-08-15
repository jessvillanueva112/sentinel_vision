# 🚨 Sentinel Vision: AI-Powered Threat Detection for School Safety

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![YOLOv5](https://img.shields.io/badge/YOLOv5-Latest-orange.svg)](https://github.com/ultralytics/yolov5)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-blue.svg)](https://opencv.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **AI-powered threat detection system for earlier safety measures in schools**

## 📖 Overview

Sentinel Vision is an innovative AI-powered threat detection system designed to enhance school safety through early threat detection and automated emergency response. Built by a student who experienced firsthand the need for better safety measures, this system uses computer vision and machine learning to detect potential threats and trigger immediate safety protocols.

### 🎯 Mission
To create safer learning environments by providing earlier awareness of potential threats, enabling faster emergency responses, and ultimately increasing the likelihood of saving lives in critical situations.

## 🚀 Key Features

- **Real-time Threat Detection**: AI-powered computer vision using YOLOv5 for immediate threat identification
- **Multi-Camera Integration**: Seamless integration with existing school security camera infrastructure
- **Automated Emergency Response**: Integrated P.A. announcements and 911 call simulation
- **Multi-Stage Safety Framework**: Formation → Detection → Action → Reaction workflow
- **Parallel Processing**: Optimized performance using multi-threading for faster detection
- **Central Control Dashboard**: Comprehensive monitoring with birds-eye view visualization
- **Role-Based Access Control**: Secure authentication for school administrators and staff
- **Sound Alert System**: Distinct audio cues for different emergency stages

## 🏗️ System Architecture

### Four-Stage Framework

1. **Formation**: Threat enters the building or incident occurs
2. **Detection**: Computer vision and ML algorithms identify specific threat types
3. **Action**: Tailored P.A. announcements with threat information and location
4. **Reaction**: Automated 911 calls with comprehensive real-time data

### Technical Components

- **YOLOv5 Object Detection**: State-of-the-art single-class detection architecture
- **OpenCV Integration**: Real-time video processing and frame analysis
- **Flask Web Framework**: Backend API and dashboard serving
- **PostgreSQL Database**: Local on-premises data storage for security and privacy
- **WebSocket Communication**: Real-time dashboard updates
- **Parallel Processing**: Multi-threaded threat detection using Amdahl's Law optimization
- **Audio Integration**: Text-to-speech and sound effect systems
- **GUI Control Interface**: Centralized monitoring and control board

## 💻 Tech Stack

### **Backend & Core**
- **Python 3.8+**: Primary programming language
- **Flask 2.0+**: Web framework for API and dashboard
- **OpenCV 4.5+**: Computer vision and video processing
- **PyTorch**: Deep learning framework for YOLOv5
- **NumPy**: Numerical computing and array operations

### **AI & Machine Learning**
- **YOLOv5**: Real-time object detection model
- **Jupyter Notebook**: Model training and experimentation
- **LabelImg**: Dataset annotation and labeling
- **Ultralytics**: YOLOv5 implementation and utilities

### **Database & Storage**
- **PostgreSQL 13+**: Primary database for detection logs and system data
- **SQLAlchemy**: Python ORM for database operations
- **Alembic**: Database migration management

### **Real-time Communication**
- **WebSocket**: Real-time dashboard updates
- **Flask-SocketIO**: WebSocket integration with Flask
- **Redis**: Optional caching and session management

### **Security & Authentication**
- **Flask-Login**: User session management
- **Flask-Security**: Role-based access control
- **JWT**: Secure token-based authentication
- **bcrypt**: Password hashing and security

### **Development & Deployment**
- **Docker**: Containerization for consistent deployment
- **Gunicorn**: WSGI server for production
- **Nginx**: Reverse proxy and static file serving
- **Supervisor**: Process management and monitoring

## 📊 Performance Metrics

### Detection Accuracy
- **mAP@0.5**: > 0.9 (90%+ accuracy)
- **mAP@0.5:0.95**: > 0.7 (70%+ accuracy across IoU thresholds)
- **IoU Threshold**: > 0.5 for accurate threat localization

### Processing Performance
- **Target Frame Rate**: 30 FPS (configurable)
- **Detection Speed**: Real-time processing with < 100ms latency
- **Parallel Speedup**: 2.11x - 2.29x improvement using multi-threading
- **Multi-Camera Support**: Up to 16 concurrent camera streams

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- CUDA-capable GPU (optional, for enhanced performance)
- Network access to existing school security cameras
- Audio output capabilities

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sentinel-vision.git
cd sentinel-vision
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL database**
```bash
# Create database and user
sudo -u postgres psql
CREATE DATABASE sentinel_vision;
CREATE USER sentinel_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE sentinel_vision TO sentinel_user;
\q
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials and camera settings
```

6. **Run database migrations**
```bash
flask db upgrade
```

7. **Download YOLOv5 weights**
```bash
cd yolov5
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt
```

8. **Train the model** (if using custom dataset)
```bash
python train.py --img 640 --batch 4 --epochs 50 --data data_v1.yaml --weights yolov5s.pt
```

9. **Launch the system**
```bash
python main.py
```

## 📁 Project Structure

```
sentinel-vision/
├── 📁 app/                    # Flask application
│   ├── 📁 models/            # Database models
│   ├── 📁 routes/            # API endpoints
│   ├── 📁 templates/         # HTML templates
│   ├── 📁 static/            # CSS, JS, images
│   └── 📁 utils/             # Utility functions
├── 📁 dataset_v1/            # Training dataset
│   ├── 📁 images/            # Training images
│   ├── 📁 labels/            # YOLO format labels
│   ├── 📁 train/             # Training split
│   └── 📁 test/              # Testing split
├── 📁 yolov5/                # YOLOv5 implementation
├── 📁 mp3_sounds/            # Audio files
├── 📁 migrations/             # Database migrations
├── 📁 tests/                  # Test suite
├── 🐍 main.py                 # Application entry point
├── 🐍 config.py               # Configuration settings
├── 🐍 requirements.txt        # Python dependencies
├── 🐍 .env.example           # Environment variables template
└── 📄 README.md               # This file
```

## 🔧 Configuration

### Environment Variables
```bash
# Database Configuration
DATABASE_URL=postgresql://sentinel_user:password@localhost/sentinel_vision
SECRET_KEY=your-secret-key-here

# Camera Configuration
CAMERA_RTSP_URLS=rtsp://camera1:554/stream1,rtsp://camera2:554/stream1
CAMERA_HTTP_URLS=http://camera3:8080/video,http://camera4:8080/video

# AI Model Configuration
MODEL_PATH=./yolov5/runs/train/exp2/weights/best.pt
CONFIDENCE_THRESHOLD=0.4
IOU_THRESHOLD=0.6

# Emergency Response Configuration
PA_ANNOUNCEMENT_ENABLED=true
AUTO_911_CALL_ENABLED=true
EMERGENCY_DELAY_SECONDS=7
```

### Model Parameters
- **Confidence Threshold**: 0.4 (configurable for precision/recall balance)
- **IoU Threshold**: 0.6 for Non-Maximum Suppression
- **Input Resolution**: 640x480 (configurable)
- **Batch Size**: 4 (adjustable based on hardware)

## 🎮 Usage

### Dashboard Access
1. **Launch the system**: `python main.py`
2. **Open browser**: Navigate to `http://localhost:5000`
3. **Login**: Use admin credentials
4. **Monitor**: View real-time camera feeds and detection results

### Dashboard Features
- **Birds-Eye View**: School-wide camera layout with threat overlays
- **Real-time Monitoring**: Live video feeds with detection bounding boxes
- **Threat Alerts**: Immediate notifications with location and details
- **System Status**: Performance metrics and health monitoring
- **User Management**: Role-based access control for staff

### Emergency Sequence
1. **Alarm Activation**: Immediate audio alert
2. **P.A. Announcement**: Tailored threat information
3. **911 Simulation**: Automated emergency call simulation
4. **Response Coordination**: Emergency services notification

## 🔬 Technical Details

### Development Approach
- **AI-Assisted Coding**: Leveraged AI tools for implementation while maintaining full control over design decisions
- **Project Management**: Handled system architecture, ethical considerations, and deployment strategy
- **Human Oversight**: All critical decisions about school safety protocols made by human judgment

### Video Processing Pipeline
1. **Camera Integration**: RTSP/HTTP stream ingestion from existing infrastructure
2. **Frame Extraction**: Real-time frame capture and buffering
3. **AI Processing**: YOLOv5 inference on GPU/CPU
4. **Threat Detection**: Confidence scoring and bounding box generation
5. **Alert Generation**: Real-time notification system

### Database Schema
```sql
-- Users and Authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Detection Events
CREATE TABLE detection_events (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(50) NOT NULL,
    threat_type VARCHAR(50) NOT NULL,
    confidence_score DECIMAL(5,4) NOT NULL,
    location_x INTEGER NOT NULL,
    location_y INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- System Logs
CREATE TABLE system_logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id)
);
```

### Performance Optimization
- **Parallel Processing**: Multi-threaded frame processing using shared memory
- **GPU Acceleration**: CUDA support for enhanced inference speed
- **Memory Management**: Efficient frame buffering and garbage collection
- **Database Optimization**: Indexed queries and connection pooling

## 🚨 Security & Privacy

### Development Ethics
- **AI Transparency**: Open about using AI as a development tool while maintaining human oversight
- **Responsible AI**: All safety-critical decisions made by human operators, not AI systems
- **Ethical Deployment**: Prioritizing student safety and privacy in all design decisions

### Data Protection
- **Local Processing**: All detection occurs on-premises
- **No Cloud Storage**: Video feeds remain within school network
- **Configurable Retention**: Customizable data storage policies
- **Encrypted Storage**: Database encryption at rest
- **Secure Authentication**: JWT tokens with role-based access

### Access Control
- **Role-based Permissions**: Different access levels for staff
- **Audit Logging**: Comprehensive activity tracking
- **Secure Configuration**: Environment variable-based secrets
- **Session Management**: Secure user sessions with timeout

## 🔮 Future Enhancements

### Planned Features
- **Multi-School Support**: Network-wide deployment capabilities
- **Behavioral Analysis**: Advanced threat pattern recognition
- **Thermal Imaging**: Enhanced detection capabilities
- **Mobile App**: Remote monitoring and control
- **API Integration**: Third-party security system integration

### Research Areas
- **False Positive Reduction**: Advanced filtering algorithms
- **Privacy-Preserving AI**: Federated learning approaches
- **Edge Computing**: Distributed processing capabilities
- **Real-time Analytics**: Advanced threat intelligence

## 📈 Impact & Goals

### Development Milestones
- **Project Management**: Successfully coordinated AI-assisted development while maintaining ethical standards
- **System Design**: Architected comprehensive safety framework balancing automation with human oversight
- **AI Integration**: Leveraged modern AI tools while ensuring human control over critical safety decisions

### Quantifiable Targets
- **Response Time Improvement**: 80-90% faster emergency response
- **Early Detection Rate**: 70-75% improvement in threat identification
- **False Alarm Reduction**: < 5% false positive rate
- **System Uptime**: 99.9% availability for critical safety functions

### Long-term Vision
- **Nationwide Deployment**: Scalable solution for schools across the country
- **Community Safety**: Enhanced security for educational institutions
- **Student Well-being**: Safer learning environments for future generations

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Philosophy
This project embraces **AI-assisted development** as a modern approach to coding. I handled the project management, system architecture, and ethical considerations, while using AI tools to help with implementation. This transparency allows us to focus on what matters most: building safer schools.

### Development Areas
- **Model Improvements**: Enhanced detection accuracy
- **UI/UX**: Better user interface design
- **Documentation**: Improved guides and tutorials
- **Testing**: Comprehensive test coverage
- **AI Ethics**: Ensuring responsible AI deployment in school environments

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🚨 Making schools safer, one detection at a time 🚨**

*Built with ❤️ for student safety and peace of mind*

</div>
