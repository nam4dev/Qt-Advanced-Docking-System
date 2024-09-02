//============================================================================
/// \file   DockComponentsFactory.cpp
/// \author Uwe Kindler
/// \date   10.02.2020
/// \brief  Implementation of DockComponentsFactory
//============================================================================

//============================================================================
//                                   INCLUDES
//============================================================================
#include <AutoHideTab.h>
#include "DockComponentsFactory.h"

#include <memory>

#include "DockWidgetTab.h"
#include "DockAreaTabBar.h"
#include "DockAreaTitleBar.h"
#include "DockWidget.h"
#include "DockAreaWidget.h"

namespace ads
{

    CDockWidgetTab* CDockComponentsFactory::createDockWidgetTab(CDockWidget* DockWidget) {
        return new CDockWidgetTab(DockWidget);
    }

    CAutoHideTab* CDockComponentsFactory::createDockWidgetSideTab(CDockWidget* DockWidget) {
        return new CAutoHideTab(DockWidget);
    }

    CDockAreaTabBar* CDockComponentsFactory::createDockAreaTabBar(CDockAreaWidget* DockArea) {
        return new CDockAreaTabBar(DockArea);
    }

    CDockAreaTitleBar* CDockComponentsFactory::createDockAreaTitleBar(CDockAreaWidget* DockArea) {
        return new CDockAreaTitleBar(DockArea);
    }

} // namespace ads

//---------------------------------------------------------------------------
// EOF DockComponentsFactory.cpp
