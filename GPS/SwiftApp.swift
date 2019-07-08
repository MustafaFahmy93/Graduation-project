//
//  ViewController.swift
//  iGP Sensors Readings
//
//  Created by Shimaa Hassan on 7/2/19.
//  Copyright © 2019 Shimaa Hassan. All rights reserved.
//

import UIKit
import CoreLocation
import FirebaseDatabase
import FirebaseAuth
import MapKit


class ViewController: UIViewController ,CLLocationManagerDelegate {
    
    @IBOutlet weak var refresh: UIButton!
    @IBOutlet weak var mapView: MKMapView!
    @IBOutlet weak var allResults: UITextView!
    @IBOutlet weak var allResult2: UITextView!
    @IBOutlet weak var OnOff: UISwitch!
    @IBOutlet weak var segment: UISegmentedControl!
    
    var ref1: DatabaseReference!
    var ref2: DatabaseReference!
    
    var locationManager = CLLocationManager()

    let cairoLoc = GPS(lat: 30.0565563, long: 31.2821563)
    var textViewText1 = String()
    var textViewText2 = String()

    override func viewDidLoad() {
        super.viewDidLoad()
        switch segment.selectedSegmentIndex {
        case 0:
            // GPS
            print("GPS")
            mapView.isHidden = false
            allResult2.isHidden = true
            allResults.isHidden = false
            reset()
        case 1:
            // compass
            print("Compass")
            mapView.isHidden = true
            allResult2.isHidden = false
            allResults.isHidden = true
            reset()
        default:
            print("None")
        }
        
    }
    func updateGPSReading(gps: GPS){
        ref1 = Database.database().reference()
        
        let newCordinate = ["/GPS/lat":  gps.lat,
                    "/GPS/long": gps.long]
        ref1.updateChildValues(newCordinate as [AnyHashable : Any])
    }
    func updateCompassReading(compass: Compass){
        ref2 = Database.database().reference()

        let newHead = ["/Compass/head": compass.head,"/Compass/x": compass.x,"/Compass/y": compass.y,"/Compass/z": compass.z]
        ref2.updateChildValues(newHead as [AnyHashable : Any])
    }
    func reset(){
        allResults.text = ""
        allResult2.text = ""
        OnOff.setOn(false, animated: true)
        OnOff.addTarget(self, action: #selector(setONOFF), for: .valueChanged)
        refresh.addTarget(self, action: #selector(refreshPressed), for: .touchUpInside)
        segment.addTarget(self, action: #selector(segmentDidChange), for: .valueChanged)
        let center = CLLocationCoordinate2D(latitude: CLLocationDegrees(cairoLoc.lat), longitude: CLLocationDegrees(cairoLoc.long))
        let region = MKCoordinateRegion(center: center, span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1))
        self.mapView.setRegion(region, animated: true)
    }
    @objc func setONOFF(_ sender: UISwitch){
        OnOff.setOn(!sender.isOn, animated: true)
        switch sender.isOn {
        case false:
            reset()
        default:
            print("work fine!")
        }
        switch segment.selectedSegmentIndex {
        case 0:
            // GPS
            if OnOff.isOn{
            setupGPS()
            }
        case 1:
            // compass
            if OnOff.isOn{
                setupCompass()
            }
        default:
            print("None")
        }
    }
    @objc func segmentDidChange(){
        switch segment.selectedSegmentIndex {
        case 0:
            // GPS
            print("GPS")
            mapView.isHidden = false
            allResult2.isHidden = true
            allResults.isHidden = false
            reset()
        case 1:
            // compass
            print("Compass")
            mapView.isHidden = true
            allResult2.isHidden = false
            allResults.isHidden = true
            reset()
        default:
            print("None")
        }
    }
    @objc func refreshPressed(){
        viewDidLoad()
    }
    func setupGPS(){
        print("setupGPS")
        locationManager.requestWhenInUseAuthorization()
        textViewText1 = "LocationAvailable: \(false)"
        if CLLocationManager.locationServicesEnabled() {
            locationManager.delegate = self
            locationManager.desiredAccuracy = kCLLocationAccuracyNearestTenMeters
            textViewText1 = "LocationAvailable: \(true) \n\n"
            textViewText1 += "Your Location: \n"
            allResults.text = textViewText1
            locationManager.startUpdatingLocation()
            textViewText1 += "\n lat: \(locationManager.location?.coordinate.latitude ?? 0), long: \(locationManager.location?.coordinate.longitude ?? 0)"
            self.allResults.text = textViewText1
        }
    }
    func setupCompass(){
        print("setupCompass")
        locationManager.requestWhenInUseAuthorization()
        locationManager.delegate = self
        locationManager.startUpdatingLocation()
        let avilable = CLLocationManager.headingAvailable()
        textViewText2 += "\nheadingAvailable: \(avilable)"
        allResult2.text = textViewText2
        if avilable{
            textViewText2 += "\n\n"
            textViewText2 += "newHeading: "
            allResult2.text = textViewText2
            locationManager.startUpdatingHeading()
            textViewText2 += "\n\nmagneticHeading:\(locationManager.heading?.magneticHeading ?? 0)"
            textViewText2 += "\nx:\(locationManager.heading?.x ?? 0)"
            textViewText2 += "\ny:\(locationManager.heading?.y ?? 0)"
            textViewText2 += "\nz:\(locationManager.heading?.z ?? 0)"
            self.allResult2.text = textViewText2
            let compass = Compass(head: locationManager.heading?.magneticHeading ?? 0.0, x: locationManager.heading?.x ?? 0.0, y: locationManager.heading?.x ?? 0.0, z: locationManager.heading?.x ?? 0.0)
            updateCompassReading(compass: compass)
            
        }
    }
    
    private func locationManager(manager: CLLocationManager!, didUpdateHeading newHeading: CLHeading!) {
        textViewText2 += "\n\nmagneticHeading:\(locationManager.heading?.magneticHeading ?? 0)"
        textViewText2 += "\nx:\(locationManager.heading?.x ?? 0)"
        textViewText2 += "\ny:\(locationManager.heading?.y ?? 0)"
        textViewText2 += "\nz:\(locationManager.heading?.z ?? 0)"
        self.allResult2.text = textViewText2
        print(newHeading.magneticHeading)
        let compass = Compass(head: newHeading.magneticHeading, x: locationManager.heading?.x ?? 0.0, y: locationManager.heading?.x ?? 0.0, z: locationManager.heading?.x ?? 0.0)
            updateCompassReading(compass: compass)
            
    }
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        setupCompass()
        guard let locValue: CLLocationCoordinate2D = manager.location?.coordinate else { return }
        print("locations = \(locValue.latitude) \(locValue.longitude)")
        textViewText1 += "\n lat: \(locValue.latitude), long: \(locValue.longitude)"
        self.allResults.text = textViewText1
        let gps = GPS(lat: locValue.latitude, long: locValue.longitude)
        updateGPSReading(gps: gps)
        
        if let location = locations.last{
            let center = CLLocationCoordinate2D(latitude: location.coordinate.latitude, longitude: location.coordinate.longitude)
            let region = MKCoordinateRegion(center: center, span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01))
            self.mapView.setRegion(region, animated: true)
            
            let annotation = MKPointAnnotation()
            annotation.coordinate = center
            annotation.title = "You"
            mapView.addAnnotation(annotation)
        }
    }
}
