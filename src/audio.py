from pathlib import Path
import pygame

ROOT_DIR = Path(__file__).resolve().parent.parent
SOUNDS_DIR = ROOT_DIR / "audio"
if not SOUNDS_DIR.exists():
    SOUNDS_DIR = ROOT_DIR / "assets" / "audio"


class SoundManager:
    """Gere o carregamento e reprodução dos efeitos sonoros com fallback seguro."""

    def __init__(self) -> None:
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.enabled: bool = True

        if not pygame.mixer.get_init():
            try:
                # Buffer baixo (512) para evitar atraso/latência no pulo
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except Exception as e:
                print(f"[ÁUDIO] Não foi possível iniciar o mixer: {e}")
                self.enabled = False
                return

        self._load_sounds()

    def _load_sounds(self) -> None:
        """Carrega os ficheiros de áudio e define os volumes individuais."""
        files = {
            "wing": "wing.wav",
            "swoosh": "swoosh.wav",
            "point": "point.wav",
            "hit": "hit.wav",
            "die": "die.wav",
        }

        volumes = {
            "wing": 0.4,
            "swoosh": 0.45,
            "point": 0.5,
            "hit": 0.6,
            "die": 0.5,
        }

        for name, filename in files.items():
            path = SOUNDS_DIR / filename
            if path.exists():
                try:
                    sound = pygame.mixer.Sound(str(path))
                    sound.set_volume(volumes.get(name, 0.5))
                    self.sounds[name] = sound
                except Exception as e:
                    print(f"[ÁUDIO] Erro ao carregar '{filename}': {e}")

    def play(self, sound_name: str) -> None:
        """Reproduz um som pelo nome caso o subsistema esteja operacional."""
        if not self.enabled:
            return
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()