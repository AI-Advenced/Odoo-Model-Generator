# -*- coding: utf-8 -*-
"""
Gestionnaire de fichiers pour Odoo Model Generator
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional
import zipfile
import tarfile

class FileManager:
    """Gestionnaire de fichiers et dossiers"""
    
    @staticmethod
    def create_directory(path: str, parents: bool = True, exist_ok: bool = True) -> Path:
        """Crée un dossier avec les options spécifiées"""
        dir_path = Path(path)
        dir_path.mkdir(parents=parents, exist_ok=exist_ok)
        return dir_path
    
    @staticmethod
    def copy_file(source: str, destination: str, create_dirs: bool = True) -> bool:
        """Copie un fichier vers une destination"""
        source_path = Path(source)
        dest_path = Path(destination)
        
        if create_dirs:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(source_path, dest_path)
            return True
        except Exception as e:
            print(f"Erreur lors de la copie: {e}")
            return False
    
    @staticmethod
    def copy_directory(source: str, destination: str) -> bool:
        """Copie un dossier complet"""
        try:
            shutil.copytree(source, destination, dirs_exist_ok=True)
            return True
        except Exception as e:
            print(f"Erreur lors de la copie du dossier: {e}")
            return False
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Supprime un fichier"""
        try:
            Path(file_path).unlink()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
    
    @staticmethod
    def delete_directory(dir_path: str) -> bool:
        """Supprime un dossier et son contenu"""
        try:
            shutil.rmtree(dir_path)
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du dossier: {e}")
            return False
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """Écrit du contenu dans un fichier"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Erreur lors de l'écriture: {e}")
            return False
    
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """Lit le contenu d'un fichier"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return None
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Vérifie si un fichier existe"""
        return Path(file_path).exists()
    
    @staticmethod
    def directory_exists(dir_path: str) -> bool:
        """Vérifie si un dossier existe"""
        return Path(dir_path).is_dir()
    
    @staticmethod
    def list_files(directory: str, pattern: str = '*', recursive: bool = False) -> List[str]:
        """Liste les fichiers dans un dossier"""
        dir_path = Path(directory)
        
        if recursive:
            files = list(dir_path.rglob(pattern))
        else:
            files = list(dir_path.glob(pattern))
        
        return [str(f) for f in files if f.is_file()]
    
    @staticmethod
    def list_directories(directory: str, pattern: str = '*') -> List[str]:
        """Liste les dossiers dans un répertoire"""
        dir_path = Path(directory)
        directories = [str(d) for d in dir_path.glob(pattern) if d.is_dir()]
        return directories
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Retourne la taille d'un fichier en octets"""
        return Path(file_path).stat().st_size
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Retourne l'extension d'un fichier"""
        return Path(file_path).suffix
    
    @staticmethod
    def change_extension(file_path: str, new_extension: str) -> str:
        """Change l'extension d'un fichier"""
        path = Path(file_path)
        return str(path.with_suffix(new_extension))
    
    @staticmethod
    def create_archive(source_dir: str, archive_path: str, 
                      format_type: str = 'zip') -> bool:
        """Crée une archive d'un dossier"""
        try:
            source_path = Path(source_dir)
            archive_path = Path(archive_path)
            
            if format_type.lower() == 'zip':
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in source_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(source_path.parent)
                            zipf.write(file_path, arcname)
            
            elif format_type.lower() in ['tar', 'tar.gz', 'tgz']:
                mode = 'w:gz' if format_type.lower() in ['tar.gz', 'tgz'] else 'w'
                with tarfile.open(archive_path, mode) as tar:
                    tar.add(source_path, arcname=source_path.name)
            
            else:
                raise ValueError(f"Format d'archive non supporté: {format_type}")
            
            return True
        except Exception as e:
            print(f"Erreur lors de la création de l'archive: {e}")
            return False
    
    @staticmethod
    def extract_archive(archive_path: str, destination: str) -> bool:
        """Extrait une archive vers un dossier"""
        try:
            archive_path = Path(archive_path)
            dest_path = Path(destination)
            dest_path.mkdir(parents=True, exist_ok=True)
            
            if archive_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zipf:
                    zipf.extractall(dest_path)
            
            elif archive_path.suffix.lower() in ['.tar', '.gz', '.tgz']:
                with tarfile.open(archive_path, 'r:*') as tar:
                    tar.extractall(dest_path)
            
            else:
                raise ValueError(f"Format d'archive non supporté: {archive_path.suffix}")
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'extraction: {e}")
            return False
    
    @staticmethod
    def create_temp_directory() -> str:
        """Crée un dossier temporaire"""
        return tempfile.mkdtemp()
    
    @staticmethod
    def cleanup_temp_directory(temp_dir: str) -> bool:
        """Nettoie un dossier temporaire"""
        return FileManager.delete_directory(temp_dir)
    
    @staticmethod
    def backup_file(file_path: str, suffix: str = '.bak') -> Optional[str]:
        """Crée une sauvegarde d'un fichier"""
        source_path = Path(file_path)
        if not source_path.exists():
            return None
        
        backup_path = source_path.with_suffix(source_path.suffix + suffix)
        
        try:
            shutil.copy2(source_path, backup_path)
            return str(backup_path)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return None
    
    @staticmethod
    def restore_backup(backup_path: str, original_path: str = None) -> bool:
        """Restaure un fichier depuis sa sauvegarde"""
        backup_path = Path(backup_path)
        
        if original_path:
            original_path = Path(original_path)
        else:
            # Déduire le chemin original en supprimant le suffixe de backup
            original_path = backup_path.with_suffix('')
            if original_path.suffix == backup_path.suffix.replace('.bak', ''):
                original_path = backup_path.with_suffix(backup_path.suffix.replace('.bak', ''))
        
        try:
            shutil.copy2(backup_path, original_path)
            return True
        except Exception as e:
            print(f"Erreur lors de la restauration: {e}")
            return False
    
    @staticmethod
    def safe_filename(filename: str) -> str:
        """Nettoie un nom de fichier pour le rendre sûr"""
        # Remplace les caractères problématiques
        safe_chars = '-_.'
        cleaned = ''.join(c if c.isalnum() or c in safe_chars else '_' for c in filename)
        
        # Supprime les underscores multiples
        while '__' in cleaned:
            cleaned = cleaned.replace('__', '_')
        
        # Supprime les underscores en début et fin
        cleaned = cleaned.strip('_')
        
        return cleaned
    
    @staticmethod
    def get_directory_size(directory: str) -> int:
        """Calcule la taille totale d'un dossier"""
        total_size = 0
        dir_path = Path(directory)
        
        for file_path in dir_path.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        return total_size
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Formate une taille en octets en format lisible"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        
        while size_bytes >= 1024.0 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"