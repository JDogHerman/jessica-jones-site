<?php
/**
 * Jessica Jones theme functions.
 *
 * @package jessica-jones
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Google Fonts used by the theme (Cormorant Garamond for headings,
 * Source Serif 4 for body text).
 */
function jessica_jones_fonts_url() {
	return 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;1,8..60,400&display=swap';
}

/**
 * Load the fonts and the theme stylesheet on the site.
 */
function jessica_jones_enqueue() {
	$version = wp_get_theme()->get( 'Version' );
	wp_enqueue_style( 'jessica-jones-fonts', jessica_jones_fonts_url(), array(), null );
	wp_enqueue_style( 'jessica-jones', get_stylesheet_uri(), array( 'jessica-jones-fonts' ), $version );
}
add_action( 'wp_enqueue_scripts', 'jessica_jones_enqueue' );

/**
 * Show the same fonts and styles inside the block editor.
 */
function jessica_jones_editor_styles() {
	add_editor_style( array( jessica_jones_fonts_url(), 'style.css' ) );
}
add_action( 'after_setup_theme', 'jessica_jones_editor_styles' );

/**
 * After the content is imported, use the page called "Home" as the
 * front page (Settings > Reading), once. If you later change that
 * setting yourself, the theme leaves it alone.
 */
function jessica_jones_set_front_page() {
	if ( get_option( 'jessica_jones_front_page_done' ) ) {
		return;
	}
	$home = get_page_by_path( 'home' );
	if ( ! $home || 'publish' !== $home->post_status ) {
		return;
	}
	update_option( 'show_on_front', 'page' );
	update_option( 'page_on_front', $home->ID );
	update_option( 'jessica_jones_front_page_done', 1 );
}
add_action( 'admin_init', 'jessica_jones_set_front_page' );
