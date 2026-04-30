use std::path::PathBuf;
use std::process::{Child, Command};
use std::sync::Mutex;
use std::thread;
use std::time::Duration;

struct BackendProcess(Mutex<Option<Child>>);

fn find_backend_dir() -> PathBuf {
    let resource_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));

    let candidates = vec![
        resource_dir.join("../../server.py"),
        resource_dir.join("server.py"),
        resource_dir.parent().unwrap().join("server.py"),
    ];

    for candidate in &candidates {
        if candidate.exists() {
            return candidate.parent().unwrap().to_path_buf();
        }
    }

    resource_dir
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .to_path_buf()
}

fn start_python_backend() -> Option<Child> {
    let backend_dir = find_backend_dir();
    println!("[tauri] Python backend dir: {:?}", backend_dir);

    let server_py = backend_dir.join("server.py");
    if !server_py.exists() {
        eprintln!("[tauri] ERROR: server.py not found at {:?}", server_py);
        return None;
    }

    match Command::new("python")
        .arg("server.py")
        .current_dir(&backend_dir)
        .spawn()
    {
        Ok(child) => {
            println!(
                "[tauri] Python backend started (PID: {})",
                child.id()
            );
            Some(child)
        }
        Err(e) => {
            eprintln!("[tauri] Failed to start Python: {}", e);
            None
        }
    }
}

#[tauri::command]
fn get_backend_status(state: tauri::State<BackendProcess>) -> bool {
    let guard = state.0.lock().unwrap();
    guard.is_some()
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let child = start_python_backend();
            app.manage(BackendProcess(Mutex::new(child)));
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![get_backend_status])
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::Destroyed = event {
                if let Some(state) = window.try_state::<BackendProcess>() {
                    if let Ok(mut guard) = state.0.lock() {
                        if let Some(ref mut child) = *guard {
                            println!("[tauri] Killing Python backend...");
                            let _ = child.kill();
                        }
                    }
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
