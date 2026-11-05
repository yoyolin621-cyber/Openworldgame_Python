673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
    }
}

document.addEventListener("keydown", e => {
    if (e.code === "KeyE" && gameStarted) {
        collectCrystal();
    }
});

// --------------------------------
// MOVEMENT AND ANIMATION
// --------------------------------

const clock = new THREE.Clock();

let velocity = new THREE.Vector3();

const WORLD_LIMIT = 112;

function animate() {

    requestAnimationFrame(animate);

    const delta = Math.min(clock.getDelta(), 0.05);
    const time = clock.elapsedTime;

    // Crystal animation
    crystals.forEach((crystal, i) => {

        if (!crystal.userData.collected) {

            crystal.rotation.y += delta;
            crystal.position.y +=
                Math.sin(time * 2 + i) * 0.003;
        }
    });

    // Player movement
    if (gameStarted) {

        const speed = keys["ShiftLeft"] ||
                      keys["ShiftRight"] ? 18 : 9;

        let forward = 0;
        let sideways = 0;

        if (keys["KeyW"]) forward += 1;
        if (keys["KeyS"]) forward -= 1;
        if (keys["KeyA"]) sideways -= 1;
        if (keys["KeyD"]) sideways += 1;

        const length = Math.sqrt(
            forward * forward +
            sideways * sideways
        );

        if (length > 0) {
            forward /= length;
            sideways /= length;
        }

        // Move relative to the direction the camera is facing.
        const moveX = Math.sin(yaw) * forward + Math.cos(yaw) * sideways;
        const moveZ = -Math.cos(yaw) * forward + Math.sin(yaw) * sideways;
        camera.position.x += moveX * speed * delta;
        camera.position.z += moveZ * speed * delta;

        // Keep the player within the world
        camera.position.x = THREE.MathUtils.clamp(
            camera.position.x,
            -WORLD_LIMIT,
            WORLD_LIMIT
        );

        camera.position.z = THREE.MathUtils.clamp(
            camera.position.z,
            -WORLD_LIMIT,
            WORLD_LIMIT
        );

        // Follow terrain elevation
        const groundY = terrainHeight(
            camera.position.x,
            camera.position.z
        );

        camera.position.y = groundY + 2.2;
    }

    renderer.render(scene, camera);
}

animate();

// --------------------------------
// RESPONSIVE SCREEN
// --------------------------------

window.addEventListener("resize", () => {

    camera.aspect =
        window.innerWidth / window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );
});

</script>

</body>
</html>
"""

# Display game
components.html(
    game_html,
    height=760,
    scrolling=False
)
