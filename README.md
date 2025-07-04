# P4CK37 GL0TT0N 🍽️
### *The Insatiable Network Devourer*

A professional network stress testing tool with advanced proxy chain support for authorized security testing and educational purposes.

## ⚡ Features

- **TCP/UDP Flood Attacks** - High-performance network stress testing
- **Proxy Chain Support** - Route attacks through SOCKS5 proxy networks
- **Multi-threaded Architecture** - Utilize hundreds of concurrent connections
- **Real-time Statistics** - Live monitoring of attack performance
- **Professional UI** - Color-coded interface with detailed reporting
- **Graceful Interruption** - Clean shutdown with Ctrl+C handling

## 🛠️ Installation

### Quick Setup
```bash
# Clone or download this folder
cd P4CK37_GL0TT0N

#Run the setup file
python setup.py

#or install the dependencies with the requirements.txt

# Install dependencies
pip install -r requirements.txt

# Run the tool
python packet_glutton.py
```

### Manual Installation
```bash
pip install colorama requests PySocks
```

## 🎯 Usage

### Basic Attack (No Proxies)
1. Run: `python packet_glutton.py`
2. Select attack type: `[1] TCP` or `[2] UDP`
3. Configure target, port, threads, packet size
4. Confirm and launch attack

### Proxy-Enhanced Attack
1. Access proxy settings: `[4] Proxy Settings`
2. Load proxies: `[2] Load from API` or `[3] Load from File`
3. Test proxy health: `[4] Test Proxy Health`
4. Enable proxy mode: `[1] Toggle Proxy Mode`
5. Return to main menu and launch TCP attack

## ⚠️ Important Notes

- **Proxies only work with TCP attacks** (UDP through SOCKS5 is unreliable)
- **Use only on networks you own** or have explicit permission to test
- **Free proxies are slow** - expect 0.5-2 packets/sec per thread
- **200+ threads recommended** for proxy attacks to maximize IP diversity

## 📊 Performance Guidelines

### Direct Attacks (No Proxies)
- **UDP**: 50-500+ packets/sec per thread
- **TCP**: 10-100 packets/sec per thread
- **Threads**: 10-50 (system dependent)

### Proxy Attacks (TCP Only)
- **Rate**: 0.5-3 packets/sec per thread
- **Threads**: 50-200 (match proxy count)
- **IPs**: Up to thread count different sources

## 🔧 Configuration

### Optimal Settings
```
TCP Proxy Attack:
- Threads: 100-200
- Packet Size: 128-256 bytes
- Duration: 2-5 minutes

UDP Direct Attack:
- Threads: 20-50
- Packet Size: 512-1024 bytes
- Duration: 30-60 seconds
```

## 📁 File Structure

- `packet_glutton.py` - Main application
- `requirements.txt` - Python dependencies
- `proxies.txt` - Optional proxy list (IP:PORT format)
- `examples/` - Sample configurations

## 🛡️ Legal & Ethical Use

This tool is intended for:
- ✅ Authorized network penetration testing
- ✅ Security research and education
- ✅ Testing your own network infrastructure
- ✅ Cybersecurity training environments

**NOT intended for:**
- ❌ Unauthorized network attacks
- ❌ Disrupting services you don't own
- ❌ Malicious activities

## 🚀 Advanced Features

### Proxy Management
- Automatic proxy health testing
- Multiple API sources for fresh proxies
- Support for custom proxy lists
- Real-time proxy rotation

### Attack Monitoring
- Live packet counters and transfer rates
- Attack duration tracking
- Final statistics reporting
- Last attack history

## 📞 Support

For issues or questions:
- Check proxy settings if TCP attacks fail
- Verify PySocks installation for proxy support
- Use direct attacks if proxy performance is too slow
- Test with smaller thread counts first

---

**Made by _GR33D_ | Use responsibly and legally**